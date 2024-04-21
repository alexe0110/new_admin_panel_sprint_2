from pydantic import BaseModel


class MoviesListApiResponse(BaseModel):
    count: int
    total_pages: int
    prev: int | None
    next: int | None
    results: list
