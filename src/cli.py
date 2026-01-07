"""
Command-line interface for QuickHelp
"""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.indexer import DocumentIndexer
from src.search import HybridSearch
from src.clustering import AutoClusterer
from src.rag import RAGSystem

console = Console()


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """
    QuickHelp - Intelligent Knowledge Base with Auto-Clustering
    
    Search and organize your personal knowledge efficiently.
    """
    pass


@cli.command()
@click.option('--path', '-p', required=True, help='Path to documents directory')
@click.option('--output', '-o', default='./data/index', help='Output directory for index')
@click.option('--recursive/--no-recursive', default=True, help='Search recursively')
def index(path, output, recursive):
    """Index documents from a directory"""
    console.print("[bold blue]Indexing documents...[/bold blue]")
    
    # Load config
    config = Config()
    
    # Create indexer
    indexer = DocumentIndexer(config)
    
    # Index documents
    try:
        documents = indexer.index_directory(path, recursive=recursive)
        
        if not documents:
            console.print("[yellow]No documents found![/yellow]")
            return
        
        # Save index
        index_path = Path(output)
        indexer.save_index(index_path / "documents.json")
        
        # Get statistics
        stats = indexer.get_statistics()
        
        # Display results
        console.print(f"\n[green]✓ Successfully indexed {stats['total_documents']} documents[/green]")
        
        table = Table(title="Indexing Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Total Documents", str(stats['total_documents']))
        table.add_row("Total Words", f"{stats['total_words']:,}")
        table.add_row("Avg Words/Doc", f"{stats['avg_words_per_doc']:.1f}")
        table.add_row("Unique Tags", str(stats['unique_tags']))
        table.add_row("Formats", ", ".join(stats['formats']))
        
        console.print(table)
        
        # Create search index
        console.print("\n[bold blue]Building search index...[/bold blue]")
        search_engine = HybridSearch(config)
        
        # Prepare chunks for indexing
        all_chunks = []
        for doc in documents:
            chunks = indexer.chunk_document(doc)
            all_chunks.extend(chunks)
        
        search_engine.index(all_chunks)
        search_engine.save(output)
        
        console.print(f"[green]✓ Search index saved to {output}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


@cli.command()
@click.argument('query')
@click.option('--mode', '-m', type=click.Choice(['keyword', 'semantic', 'hybrid']), 
              default='hybrid', help='Search mode')
@click.option('--max-results', '-n', default=10, help='Maximum number of results')
@click.option('--index-path', default='./data/index', help='Path to search index')
def search(query, mode, max_results, index_path):
    """Search the knowledge base"""
    console.print(f"[bold blue]Searching for:[/bold blue] {query}")
    console.print(f"[dim]Mode: {mode}[/dim]\n")
    
    try:
        # Load config
        config = Config()
        
        # Load search engine
        search_engine = HybridSearch(config)
        search_engine.load(index_path)
        
        # Perform search
        results = search_engine.search(query, mode=mode, max_results=max_results)
        
        if not results:
            console.print("[yellow]No results found[/yellow]")
            return
        
        # Display results
        console.print(f"[green]Found {len(results)} results:[/green]\n")
        
        for i, result in enumerate(results, 1):
            doc = result['document']
            score = result['score']
            
            # Extract metadata
            metadata = doc.get('metadata', {})
            title = metadata.get('title', 'Untitled')
            path = metadata.get('path', '')
            tags = metadata.get('tags', [])
            
            # Create panel
            content_preview = doc.get('content', '')[:200] + "..."
            
            panel_content = f"[bold]{title}[/bold]\n"
            panel_content += f"[dim]Path: {path}[/dim]\n"
            if tags:
                panel_content += f"[dim]Tags: {', '.join(tags)}[/dim]\n"
            panel_content += f"\n{content_preview}"
            
            panel = Panel(
                panel_content,
                title=f"Result {i} (Score: {score:.3f})",
                border_style="blue"
            )
            console.print(panel)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


@cli.command()
@click.option('--index-path', default='./data/index', help='Path to index')
@click.option('--output', default='./data/clusters', help='Output directory for clusters')
@click.option('--algorithm', type=click.Choice(['kmeans', 'hierarchical', 'hdbscan']),
              default='hdbscan', help='Clustering algorithm')
def cluster(index_path, output, algorithm):
    """Automatically cluster documents into categories"""
    console.print("[bold blue]Auto-clustering documents...[/bold blue]")
    
    try:
        # Load config
        config = Config()
        config.set('clustering.algorithm', algorithm)
        
        # Load documents
        indexer = DocumentIndexer(config)
        indexer.load_index(Path(index_path) / "documents.json")
        
        if not indexer.documents:
            console.print("[yellow]No documents found in index. Run 'index' command first.[/yellow]")
            return
        
        # Prepare documents for clustering
        docs_for_clustering = [
            {
                'content': doc.content,
                'metadata': {
                    'title': doc.title,
                    'path': doc.path,
                    'tags': doc.tags
                }
            }
            for doc in indexer.documents
        ]
        
        # Perform clustering
        clusterer = AutoClusterer(config)
        result = clusterer.fit(docs_for_clustering)
        
        # Save results
        output_path = Path(output)
        clusterer.save(output_path)
        
        # Display results
        console.print(f"\n[green]✓ Created {result['num_clusters']} clusters[/green]\n")
        
        summary = clusterer.get_cluster_summary()
        console.print(Panel(summary, title="Cluster Summary", border_style="green"))
        
        console.print(f"\n[dim]Results saved to {output_path}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


@cli.command()
@click.argument('question')
@click.option('--mode', '-m', type=click.Choice(['keyword', 'semantic', 'hybrid']),
              default='hybrid', help='Search mode')
@click.option('--index-path', default='./data/index', help='Path to search index')
def ask(question, mode, index_path):
    """Ask a question about your documents"""
    console.print(f"[bold blue]Question:[/bold blue] {question}\n")
    
    try:
        # Load config
        config = Config()
        
        # Load search engine
        search_engine = HybridSearch(config)
        search_engine.load(index_path)
        
        # Create RAG system
        rag_system = RAGSystem(config, search_engine)
        
        # Ask question
        with console.status("[bold blue]Thinking...[/bold blue]"):
            result = rag_system.ask(question, search_mode=mode)
        
        if not result['success']:
            console.print(f"[yellow]{result['answer']}[/yellow]")
            return
        
        # Display answer
        answer_panel = Panel(
            result['answer'],
            title="Answer",
            border_style="green"
        )
        console.print(answer_panel)
        
        # Display sources
        if result.get('sources'):
            console.print(f"\n[bold]Sources ({len(result['sources'])}):[/bold]")
            
            for source in result['sources']:
                source_text = f"[{source['id']}] {source['title']}"
                if source.get('path'):
                    source_text += f"\n    Path: {source['path']}"
                if source.get('tags'):
                    source_text += f"\n    Tags: {', '.join(source['tags'])}"
                source_text += f"\n    Relevance: {source['score']:.3f}"
                
                console.print(f"  {source_text}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


@cli.command()
@click.option('--index-path', default='./data/index', help='Path to index')
def stats(index_path):
    """Show statistics about the knowledge base"""
    try:
        # Load config
        config = Config()
        
        # Load documents
        indexer = DocumentIndexer(config)
        indexer.load_index(Path(index_path) / "documents.json")
        
        if not indexer.documents:
            console.print("[yellow]No documents found in index.[/yellow]")
            return
        
        # Get statistics
        stats = indexer.get_statistics()
        
        # Create table
        table = Table(title="Knowledge Base Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Total Documents", str(stats['total_documents']))
        table.add_row("Total Words", f"{stats['total_words']:,}")
        table.add_row("Avg Words/Doc", f"{stats['avg_words_per_doc']:.1f}")
        table.add_row("Total Tags", str(stats['total_tags']))
        table.add_row("Unique Tags", str(stats['unique_tags']))
        table.add_row("Formats", ", ".join(stats['formats']))
        
        console.print(table)
        
        # Show recent documents
        console.print("\n[bold]Recent Documents:[/bold]")
        recent_docs = sorted(indexer.documents, 
                           key=lambda d: d.updated_at, 
                           reverse=True)[:5]
        
        for doc in recent_docs:
            console.print(f"  • {doc.title} ({doc.word_count} words)")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == '__main__':
    cli()
