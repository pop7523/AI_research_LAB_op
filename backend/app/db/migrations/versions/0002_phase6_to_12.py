"""phase 6 to 12 schema

Revision ID: 0002_phase6_to_12
Revises: 0001_initial
Create Date: 2026-05-26
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_phase6_to_12"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        sa.Column("actor_type", sa.String(length=64), nullable=False),
        sa.Column("actor_name", sa.String(length=128), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("target_type", sa.String(length=64), nullable=False),
        sa.Column("target_id", sa.String(length=36), nullable=False),
        sa.Column("input_refs", sa.JSON(), nullable=True),
        sa.Column("output_summary", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "events",
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("event_time", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "issues",
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("issue_type", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("priority", sa.String(length=64), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(), nullable=True),
        sa.Column("last_updated_at", sa.DateTime(), nullable=True),
        sa.Column("editorial_reason", sa.Text(), nullable=True),
        sa.Column("uncertainty_note", sa.Text(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "facts",
        sa.Column("article_id", sa.String(length=36), nullable=False),
        sa.Column("sentence_id", sa.String(length=36), nullable=True),
        sa.Column("subject_entity_id", sa.String(length=36), nullable=True),
        sa.Column("predicate", sa.Text(), nullable=False),
        sa.Column("object_entity_id", sa.String(length=36), nullable=True),
        sa.Column("object_text", sa.Text(), nullable=True),
        sa.Column("value", sa.Numeric(), nullable=True),
        sa.Column("unit", sa.String(length=64), nullable=True),
        sa.Column("currency", sa.String(length=16), nullable=True),
        sa.Column("time_scope", sa.Text(), nullable=True),
        sa.Column("normalized_time_start", sa.DateTime(), nullable=True),
        sa.Column("normalized_time_end", sa.DateTime(), nullable=True),
        sa.Column("evidence_text", sa.Text(), nullable=False),
        sa.Column("evidence_span", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("verification_status", sa.String(length=64), nullable=False),
        sa.Column("evidence_level", sa.String(length=64), nullable=True),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("length(trim(evidence_text)) > 0"),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.ForeignKeyConstraint(["object_entity_id"], ["entities.id"]),
        sa.ForeignKeyConstraint(["sentence_id"], ["article_sentences.id"]),
        sa.ForeignKeyConstraint(["subject_entity_id"], ["entities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_facts_article_id"), "facts", ["article_id"], unique=False)
    op.create_table(
        "claims",
        sa.Column("article_id", sa.String(length=36), nullable=False),
        sa.Column("sentence_id", sa.String(length=36), nullable=True),
        sa.Column("speaker_entity_id", sa.String(length=36), nullable=True),
        sa.Column("speaker_text", sa.Text(), nullable=True),
        sa.Column("speaker_type", sa.String(length=64), nullable=True),
        sa.Column("claim_type", sa.String(length=64), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("related_entity_ids", sa.JSON(), nullable=True),
        sa.Column("evidence_text", sa.Text(), nullable=False),
        sa.Column("evidence_span", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("claim_status", sa.String(length=64), nullable=False),
        sa.Column("possible_incentive", sa.Text(), nullable=True),
        sa.Column("needs_independent_verification", sa.Boolean(), nullable=False),
        sa.Column("needs_review", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("length(trim(evidence_text)) > 0"),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.ForeignKeyConstraint(["sentence_id"], ["article_sentences.id"]),
        sa.ForeignKeyConstraint(["speaker_entity_id"], ["entities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_claims_article_id"), "claims", ["article_id"], unique=False)
    op.create_table(
        "event_links",
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("fact_id", sa.String(length=36), nullable=True),
        sa.Column("claim_id", sa.String(length=36), nullable=True),
        sa.Column("article_id", sa.String(length=36), nullable=False),
        sa.Column("relation_type", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.ForeignKeyConstraint(["claim_id"], ["claims.id"]),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["fact_id"], ["facts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_event_links_article_id"), "event_links", ["article_id"], unique=False)
    op.create_index(op.f("ix_event_links_event_id"), "event_links", ["event_id"], unique=False)
    op.create_table(
        "issue_links",
        sa.Column("issue_id", sa.String(length=36), nullable=False),
        sa.Column("article_id", sa.String(length=36), nullable=True),
        sa.Column("event_id", sa.String(length=36), nullable=True),
        sa.Column("fact_id", sa.String(length=36), nullable=True),
        sa.Column("claim_id", sa.String(length=36), nullable=True),
        sa.Column("link_type", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(["article_id"], ["articles.id"]),
        sa.ForeignKeyConstraint(["claim_id"], ["claims.id"]),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["fact_id"], ["facts.id"]),
        sa.ForeignKeyConstraint(["issue_id"], ["issues.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_issue_links_issue_id"), "issue_links", ["issue_id"], unique=False)
    op.create_table(
        "perspectives",
        sa.Column("issue_id", sa.String(length=36), nullable=False),
        sa.Column("perspective_type", sa.String(length=64), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("evidence_refs", sa.JSON(), nullable=True),
        sa.Column("weaknesses", sa.JSON(), nullable=True),
        sa.Column("affected_stakeholders", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["issues.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_perspectives_issue_id"), "perspectives", ["issue_id"], unique=False)
    op.create_table(
        "reports",
        sa.Column("issue_id", sa.String(length=36), nullable=False),
        sa.Column("report_type", sa.String(length=64), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("body_markdown", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("evidence_checked", sa.Boolean(), nullable=False),
        sa.Column("balance_checked", sa.Boolean(), nullable=False),
        sa.Column("editor_approved", sa.Boolean(), nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["issues.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reports_issue_id"), "reports", ["issue_id"], unique=False)
    op.create_table(
        "review_items",
        sa.Column("target_type", sa.String(length=64), nullable=False),
        sa.Column("target_id", sa.String(length=36), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("reviewer_note", sa.Text(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("target_type", "target_id", "status"),
    )


def downgrade() -> None:
    op.drop_table("review_items")
    op.drop_index(op.f("ix_reports_issue_id"), table_name="reports")
    op.drop_table("reports")
    op.drop_index(op.f("ix_perspectives_issue_id"), table_name="perspectives")
    op.drop_table("perspectives")
    op.drop_index(op.f("ix_issue_links_issue_id"), table_name="issue_links")
    op.drop_table("issue_links")
    op.drop_index(op.f("ix_event_links_event_id"), table_name="event_links")
    op.drop_index(op.f("ix_event_links_article_id"), table_name="event_links")
    op.drop_table("event_links")
    op.drop_index(op.f("ix_claims_article_id"), table_name="claims")
    op.drop_table("claims")
    op.drop_index(op.f("ix_facts_article_id"), table_name="facts")
    op.drop_table("facts")
    op.drop_table("issues")
    op.drop_table("events")
    op.drop_table("audit_logs")

