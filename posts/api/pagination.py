from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
	)


class PostLimitOffsetPagination(LimitOffsetPagination): #custom class to override default settings
	default_limit = 10
	max_limit = 10

class PostPageNumberPagination(PageNumberPagination):
	page_size = 20



"""
Example offset limit returned data:

{
    "count": 8,
    "next": "http://127.0.0.1:8000/api/posts/?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "user": 2,
            "title": "another post",
            "slug": "another-post",
            "content": "The ash of stellar alchemy hearts of the stars inconspicuous motes of rock and gas cosmos venture are creatures of the cosmos from which we spring.",
            "publish": "2018-03-07"
        },
        {
            "user": 2,
            "title": "new post right user",
            "slug": "new-post",
            "content": ". Culture laws of physics, inconspicuous motes of rock and gas rogue, paroxysm of global death the ash of stellar alchemy the sky calls to us not a sunrise but a galaxyrise Rig Veda.",
            "publish": "2018-03-18"
        }
    ]
}


Example of page post returned data

{
    "count": 8,
    "next": "http://127.0.0.1:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "user": 2,
            "title": "another post",
            "slug": "another-post",
            "content": "The ash of stellar alchemy hearts of the stars inconspicuous motes of rock and gas cosmos venture are creatures of the cosmos from which we spring.",
            "publish": "2018-03-07"
        },
        {
            "user": 2,
            "title": "new post right user",
            "slug": "new-post",
            "content": ". Culture laws of physics, inconspicuous motes of rock and gas rogue, paroxysm of global death the ash of stellar alchemy the sky calls to us not a sunrise but a galaxyrise Rig Veda.",
            "publish": "2018-03-18"
        }
    ]
}

"""
