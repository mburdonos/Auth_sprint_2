FILM_WORK = """
SELECT
    fw.id,
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    fw.created,
    fw.modified,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'person_role', pfw.role,
                'person_id', p.id,
                'person_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null),
        '[]'
    ) as persons,
    array_agg(DISTINCT g.name) as genres
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > '{}'
GROUP BY fw.id
ORDER BY fw.modified
"""

PERSON = """
select
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   fw.created,
   fw.modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   array_agg(DISTINCT g.name) as genres
FROM content.person p
LEFT JOIN content.person_film_work pfw ON pfw.person_id  = p.id
LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE p.modified > '{}'
GROUP BY fw.id
ORDER BY fw.modified
"""

GENRE = """
select
    fw.id,
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    fw.created,
    fw.modified,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'person_role', pfw.role,
                'person_id', p.id,
                'person_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null),
        '[]'
    ) as persons,
    array_agg(DISTINCT g.name) as genres
FROM content.genre g
LEFT JOIN content.genre_film_work gfw ON gfw.genre_id = g.id
LEFT JOIN content.film_work fw ON fw.id = gfw.film_work_id
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
WHERE g.modified > '{}'
GROUP BY fw.id
ORDER BY fw.modified
"""

person_film_work = """
SELECT
    p.id,
    p.full_name,
    array_agg(DISTINCT fw.id) FILTER (WHERE pfw.role='actor') as actors,
    array_agg(DISTINCT fw.id) FILTER (WHERE pfw.role='writer') as writers,
    array_agg(DISTINCT fw.id) FILTER (WHERE pfw.role='director') as directors,
    p.created,
    p.modified
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
WHERE fw.modified > '{}'
GROUP BY p.id
ORDER BY p.modified
"""

person_person = """
SELECT
    p.id,
    p.full_name,
    array_agg(DISTINCT fw.id) FILTER (WHERE pfw.role='actor') as actors,
    array_agg(DISTINCT fw.id) FILTER (WHERE pfw.role='writer') as writers,
    array_agg(DISTINCT fw.id) FILTER (WHERE pfw.role='director') as directors,
    p.created,
    p.modified
FROM content.person p
LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
WHERE p.modified > '{}'
GROUP BY p.id
ORDER BY p.modified
"""

genre_genre = """
SELECT
    g.id,
    g.name,
    array_agg(DISTINCT fw.id)  as film_ids,
    g.created,
    g.modified
FROM content.genre g
LEFT JOIN content.genre_film_work gfw ON gfw.genre_id = g.id
LEFT JOIN content.film_work fw ON fw.id = gfw.film_work_id
WHERE g.modified > '{}'
GROUP BY g.id
ORDER BY g.modified
"""

genre_film_work = """
SELECT
    g.id,
    g.name,
    array_agg(DISTINCT fw.id)  as film_ids,
    g.created,
    g.modified
FROM content.film_work fw
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > '{}'
GROUP BY g.id
ORDER BY g.modified
"""

GET_MOVES_FROM = {
    "film_work": FILM_WORK,
    "person": PERSON,
    "genre": GENRE,
    "person_film_work": person_film_work,
    "person_person": person_person,
    "genre_genre": genre_genre,
    "genre_film_work": genre_film_work,
}

GET_MODIFIED_DATE = """select
t.modified
from content.{} t
order by t.modified desc
limit 1;"""

CHECK_DATA = """select
count(*)
from content.{} t
where t.modified > '{}\'"""
