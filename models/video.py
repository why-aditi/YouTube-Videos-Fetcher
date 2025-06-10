from datetime import datetime
from typing import Optional, List, Any, Annotated
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId class that works with Pydantic JSON schema generation"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: Any
    ) -> JsonSchemaValue:
        return {"type": "string", "format": "objectid"}


class VideoThumbnail(BaseModel):
    url: str
    width: int
    height: int


class VideoThumbnails(BaseModel):
    default: Optional[VideoThumbnail] = None
    medium: Optional[VideoThumbnail] = None
    high: Optional[VideoThumbnail] = None
    standard: Optional[VideoThumbnail] = None
    maxres: Optional[VideoThumbnail] = None


class VideoModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, PyObjectId: str}
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    video_id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    published_at: datetime = Field(..., description="Video publish datetime")
    channel_id: str = Field(..., description="Channel ID")
    channel_title: str = Field(..., description="Channel title")
    thumbnails: VideoThumbnails = Field(..., description="Video thumbnails")
    duration: Optional[str] = Field(None, description="Video duration")
    view_count: Optional[int] = Field(None, description="View count")
    like_count: Optional[int] = Field(None, description="Like count")
    comment_count: Optional[int] = Field(None, description="Comment count")
    tags: List[str] = Field(default_factory=list, description="Video tags")
    category_id: Optional[str] = Field(None, description="Video category ID")
    language: Optional[str] = Field(None, description="Video language")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Record update time")


class VideoResponse(BaseModel):
    videos: List[VideoModel]
    total: int
    page: int
    per_page: int
    total_pages: int


class VideoFilter(BaseModel):
    search: Optional[str] = None
    channel_id: Optional[str] = None
    published_after: Optional[datetime] = None
    published_before: Optional[datetime] = None
    min_duration: Optional[int] = None
    max_duration: Optional[int] = None