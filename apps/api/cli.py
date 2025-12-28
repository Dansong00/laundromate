# apps/api/cli.py
import subprocess
from pathlib import Path

import typer

app = typer.Typer(help="🧺 LaundroMate Database Migration CLI")


def check_alembic() -> None:
    """Check if alembic is available"""
    if not Path("alembic.ini").exists():
        typer.echo("❌ Error: alembic.ini not found. Run 'alembic init alembic' first.")
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """Show current migration status"""
    check_alembic()
    typer.echo("📊 Migration Status")
    typer.echo("==================")

    # Get current version
    result = subprocess.run(["alembic", "current"], capture_output=True, text=True)
    if result.returncode == 0:
        typer.echo(f"✅ Current: {result.stdout.strip()}")
    else:
        typer.echo("❌ No migrations applied")

    # Check for pending migrations
    typer.echo("\n🔍 Checking for pending migrations...")
    subprocess.run(["alembic", "check"])


@app.command()
def create(message: str) -> None:
    """Create new migration with autogenerate"""
    check_alembic()
    typer.echo(f"�� Creating migration: {message}")

    result = subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])
    if result.returncode == 0:
        typer.echo("✅ Migration created successfully!")
        typer.echo("\n💡 Next steps:")
        typer.echo("  1. Review the generated migration file")
        typer.echo("  2. Apply with: migrate up")
    else:
        typer.echo("❌ Failed to create migration")
        raise typer.Exit(1)


@app.command()
def up(revision: str = "head") -> None:
    """Apply migrations (default: all pending)"""
    check_alembic()
    typer.echo(f"🚀 Applying migrations up to: {revision}")

    if typer.confirm("Continue?"):
        result = subprocess.run(["alembic", "upgrade", revision])
        if result.returncode == 0:
            typer.echo("✅ Migrations applied successfully!")
        else:
            typer.echo("❌ Failed to apply migrations")
            raise typer.Exit(1)


@app.command()
def down(revision: str = "-1") -> None:
    """Rollback migrations (default: one step)"""
    check_alembic()
    typer.echo(f"⏪ Rolling back to: {revision}")

    if typer.confirm("Continue?"):
        result = subprocess.run(["alembic", "downgrade", revision])
        if result.returncode == 0:
            typer.echo("✅ Migrations rolled back successfully!")
        else:
            typer.echo("❌ Failed to rollback migrations")
            raise typer.Exit(1)


@app.command()
def reset() -> None:
    """Reset database to base (WARNING: destructive!)"""
    check_alembic()
    typer.echo("⚠️  WARNING: This will reset your database to base state!")
    typer.echo("⚠️  All data will be lost!")

    if typer.confirm("Are you absolutely sure?", default=False):
        if typer.confirm("Type 'RESET' to confirm", default=False):
            typer.echo("�� Resetting database to base...")
            result = subprocess.run(["alembic", "downgrade", "base"])
            if result.returncode == 0:
                typer.echo("✅ Database reset successfully!")
                typer.echo("\n💡 Next steps:")
                typer.echo(
                    "  1. Create new migration: migrate create 'Initial migration'"
                )
                typer.echo("  2. Apply migration: migrate up")
            else:
                typer.echo("❌ Failed to reset database")
                raise typer.Exit(1)


@app.command()
def fresh() -> None:
    """Fresh start: reset + recreate + apply"""
    check_alembic()
    typer.echo("�� Fresh start: Reset + Recreate + Apply")

    if typer.confirm(
        "This will reset everything and start fresh. Continue?", default=False
    ):
        # Reset to base
        typer.echo("🔄 Resetting to base...")
        subprocess.run(["alembic", "downgrade", "base"])

        # Remove old migration files
        typer.echo("🗑️  Removing old migration files...")
        versions_dir = Path("alembic/versions")
        if versions_dir.exists():
            for file in versions_dir.glob("*"):
                file.unlink()

        # Create new initial migration
        typer.echo("📝 Creating initial migration...")
        subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "Initial migration"]
        )

        # Apply the migration
        typer.echo("🚀 Applying initial migration...")
        result = subprocess.run(["alembic", "upgrade", "head"])
        if result.returncode == 0:
            typer.echo("✅ Fresh start completed successfully!")
        else:
            typer.echo("❌ Fresh start failed")
            raise typer.Exit(1)


if __name__ == "__main__":
    app()
