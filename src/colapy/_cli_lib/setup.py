import click
import jinja2
import textwrap

from pathlib import Path

from .common import cli
from .sources_templates import CMAKE_TEMPLATE, GIT_IGNORE_TEMPLATE


@cli.group()
def setup():
    pass


@setup.command()
@click.option('--name', required=True, help='Project name')
@click.option('--prefix', default='./', help='Installation prefix directory', show_default=True)
@click.option('--version', default='1.0.0', help='Project version', show_default=True)
@click.option('--force', is_flag=True, help='Overwrite existing files')
@click.pass_context
def project(ctx: click.Context, name: str, prefix: str, version: str, force: bool):
    prefix_path = Path(prefix)

    if prefix_path.exists() and any(prefix_path.iterdir()) and not force:
        click.confirm(
            f"Directory '{prefix}' is not empty. Continue and overwrite files?",
            abort=True,
        )

    try:
        ctx.invoke(cmake, name, prefix, version)

        ctx.invoke(sources, name, prefix)

        ctx.invoke(git, prefix)

        click.echo("✅ Project setup completed successfully!")

    except Exception as e:
        click.echo(f"❌ Error during project setup: {e}", err=True)
        raise click.Abort()


@setup.command()
@click.option('--name', required=True, help='Project name')
@click.option('--prefix', default='./', help='Target directory', show_default=True)
@click.option('--version', default='1.0.0', help='Project version', show_default=True)
def cmake(name: str, prefix: str, version: str):
    try:
        data_dir = Path(prefix) / 'data'
        data_dir.mkdir(parents=True, exist_ok=True)

        config_file = data_dir / f'{name}Config.cmake.in'
        config_content = textwrap.dedent(f'''
            @PACKAGE_INIT@

            find_package(COLA REQUIRED) # COLA requirement
            #find_package(ROOT) (additional requirements)

            include(@CMAKE_INSTALL_PREFIX@/lib/cmake/{name}/{name}Export.cmake)
            #set_and_check(...), etc.
            '''
        ).lstrip()

        config_file.write_text(config_content)

        click.echo(f"✓ Created CMake config: {config_file}")

        template: jinja2.Template = jinja2.Template(CMAKE_TEMPLATE)

        cmake_path = Path(prefix) / 'CMakeLists.txt'
        cmake_content = template.render(
            module_name=name,
            version=version,
        )

        cmake_path.write_text(cmake_content)
        click.echo(f"✓ Created CMakeLists.txt: {cmake_path}")

        click.echo("✅ CMake files generated successfully!")
    except Exception as e:
        click.echo(f"❌ Error generating CMake files: {e}", err=True)
        raise click.Abort()


@setup.command()
@click.option('--name', required=True, help='Project name')
@click.option('--prefix', default='./', help='Target directory', show_default=True)
def sources(name: str, prefix: str):
    click.echo(f"Generating source files for '{name}'...")

    try:
        include_dir = Path(prefix) / 'include'
        src_dir = Path(prefix) / 'src'

        include_dir.mkdir(parents=True, exist_ok=True)
        src_dir.mkdir(parents=True, exist_ok=True)

        # Module file
        main_header = include_dir / f'{name}.hh'
        main_header.write_text(textwrap.dedent('''
            #pragma once

            #include <COLA.hh>
            #include "factory.hh"
            #include "filter.hh"
            '''
        ).lstrip())

        # Filter files
        filter_header = include_dir / 'filter.hh'
        filter_header.write_text('#pragma once\n')

        filter_source = src_dir / 'filter.cpp'
        filter_source.write_text(textwrap.dedent('''
            #include "filter.hh"
            '''
        ).lstrip())

        # Factory files
        factory_header = include_dir / 'factory.hh'
        factory_header.write_text('#pragma once\n')

        factory_source = src_dir / 'factory.cpp'
        factory_source.write_text(textwrap.dedent('''
            #include "filter.hh"
            #include "factory.hh"
            '''
        ).lstrip())

        for file in [
            main_header,
            filter_header,
            filter_source,
            factory_header,
            factory_source,
        ]:
            click.echo(f"✓ Created source file: {file}")

        click.echo("✅ Source files generated successfully!")
    except Exception as e:
        click.echo(f"❌ Error generating source files: {e}", err=True)
        raise click.Abort()


@setup.command()
@click.option('--prefix', default='./', help='Target directory', show_default=True)
def git(prefix: str):
    click.echo("Setting up Git...")
    git_file_path = Path(prefix) / '.gitignore'

    with open(git_file_path, 'w') as f:
        f.write(GIT_IGNORE_TEMPLATE)

    click.echo(f"✓ Created: {git_file_path}")
    click.echo("✅ Git setup completed!")


@cli.command()
def version():
    click.echo("COLA Project Setup CLI v1.0.0")
