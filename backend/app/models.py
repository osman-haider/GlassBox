"""
Request/response models for GlassBox.

Kept deliberately small: four inputs in, one estimate payload out.
"""

from typing import List, Literal

from pydantic import BaseModel, Field

FunnelStage = Literal["checkout", "quiz", "intake"]
FollowUpMethod = Literal["none", "email_only", "automated_sms"]


class EstimateRequest(BaseModel):
    monthly_abandoned_leads: float = Field(
        ..., gt=0, le=1_000_000, description="Estimated abandoned leads per month"
    )
    average_order_value: float = Field(
        ..., gt=0, le=1_000_000, description="Average order value in USD"
    )
    funnel_stage: FunnelStage = Field(
        ..., description="Where most leads drop off: checkout, quiz, or intake"
    )
    follow_up_method: FollowUpMethod = Field(
        ..., description="What currently happens after a lead abandons"
    )


class FeedEntry(BaseModel):
    name: str
    plan_label: str
    channel: str
    time_ago: str
    amount: float


class ConversationMessage(BaseModel):
    sender: Literal["rep", "lead"]
    text: str


class EstimateResponse(BaseModel):
    conservative_monthly_revenue: float
    expected_monthly_revenue: float
    conservative_recovered_leads: float
    expected_recovered_leads: float
    sample_feed: List[FeedEntry]
    sample_conversation: List[ConversationMessage]
    disclaimer: str
