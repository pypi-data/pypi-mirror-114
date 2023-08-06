import fastasplitter_splitter.splitter
import click


def echo_supported_fasta_file_extensions(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    supported_fasta_file_extensions = str(fastasplitter_splitter.splitter.get_supported_fasta_file_extensions()) \
        .replace("[", "").replace("]", "").replace("'", "")
    supported_fasta_file_extensions_message = "Supported fasta file extensions: {0}" \
        .format(supported_fasta_file_extensions)
    click.echo(supported_fasta_file_extensions_message)
    ctx.exit(0)


@click.group()
@click.version_option(package_name="fasta-splitter", message="%(prog)s version %(version)s")
@click.option("--supported-extensions",
              callback=echo_supported_fasta_file_extensions,
              is_flag=True,
              expose_value=False,
              is_eager=True,
              help="Show the supported fasta file extensions and exit.")
def main_group():
    """
    Command line tool to split one multiple sequences fasta file into individual sequences fasta files.
    """


main_group.add_command(fastasplitter_splitter.splitter.split)
