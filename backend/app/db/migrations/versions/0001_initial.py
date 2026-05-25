"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-26
"""

import sqlalchemy as sa
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("credibility_level", sa.String(length=64), nullable=True),
        sa.Column("credibility_score", sa.Float(), nullable=True),
        sa.Column("political_bias_note", sa.Text(), nullable=True),
        sa.Column("business_incentive_note", sa.Text(), nullable=True),
        sa.Column("is_official", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "entities",
        sa.Column("canonical_name", sa.Text(), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("country", sa.String(length=64), nullable=True),
        sa.Column("industry", sa.String(length=128), nullable=True),
        sa.Column("ticker", sa.String(length=32), nullable=True),
        sa.Column("external_ids", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_entities_ticker"), "entities", ["ticker"], unique=False)
    op.create_table(
        "articles",
        sa.Column("source_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("author", sa.Text(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("collected_at", sa.DateTime(), nullable=True),
        sa.Column("raw_html_path", sa.Text(), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("clean_text", sa.Text(), nullable=True),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("duplicate_of", sa.String(length=36), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["duplicate_of"], ["articles.id"]),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_index(op.f("ix_articles_content_hash"), "articles", ["content_hash"], unique=False)
    op.create_table(
        "entity_aliases",
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("alias", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=16), nullable=True),
        sa.Column("alias_type", sa.String(length=64), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entity_id", "alias", "language"),
    )
    op.create_index(op.f("ix_entity_aliases_alias"), "entity_aliases", ["alias"], unique=False)
    op.create_index(
        op.f("ix_entity_aliases_entity_id"),
        "entity_aliases",
        ["entity_id"],
        unique=False,
    )
    op.create_table(
        "article_sentences",
        sa.Column("article_id", sa.String(length=36), nullable=False),
        sa.Column("paragraph_index", sa.Integer(), nullable=False),
        sa.Column("sentence_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("start_offset", sa.Integer(), nullable=False),
        sa.Column("end_offset", sa.Integer(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_article_sentences_article_id"),
        "article_sentences",
        ["article_id"],
        unique=False,
    )
    op.create_table(
        "mentions",
        sa.Column("article_id", sa.String(length=36), nullable=False),
        sa.Column("sentence_id", sa.String(length=36), nullable=True),
        sa.Column("mention_text", sa.Text(), nullable=False),
        sa.Column("mention_type", sa.String(length=64), nullable=True),
        sa.Column("sentence", sa.Text(), nullable=True),
        sa.Column("paragraph_index", sa.Integer(), nullable=True),
        sa.Column("start_offset", sa.Integer(), nullable=True),
        sa.Column("end_offset", sa.Integer(), nullable=True),
        sa.Column("linked_entity_id", sa.String(length=36), nullable=True),
        sa.Column("linking_status", sa.String(length=64), nullable=False),
        sa.Column("linking_confidence", sa.Float(), nullable=True),
        sa.Column("linking_reason", sa.Text(), nullable=True),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.ForeignKeyConstraint(["linked_entity_id"], ["entities.id"]),
        sa.ForeignKeyConstraint(["sentence_id"], ["article_sentences.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_mentions_article_id"), "mentions", ["article_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_mentions_article_id"), table_name="mentions")
    op.drop_table("mentions")
    op.drop_index(op.f("ix_article_sentences_article_id"), table_name="article_sentences")
    op.drop_table("article_sentences")
    op.drop_index(op.f("ix_entity_aliases_entity_id"), table_name="entity_aliases")
    op.drop_index(op.f("ix_entity_aliases_alias"), table_name="entity_aliases")
    op.drop_table("entity_aliases")
    op.drop_index(op.f("ix_articles_content_hash"), table_name="articles")
    op.drop_table("articles")
    op.drop_index(op.f("ix_entities_ticker"), table_name="entities")
    op.drop_table("entities")
    op.drop_table("sources")
