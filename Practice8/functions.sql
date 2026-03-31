-- 1. search by pattern


CREATE OR REPLACE FUNCTION search_pattern(p_pattern TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || p_pattern || '%'
       OR p.phone ILIKE '%' || p_pattern || '%';
END;
$$;



-- 4. pagination


CREATE OR REPLACE FUNCTION paginate(limit_count INT, offset_count INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR)
LANGUAGE plpgsql AS
$$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone
    FROM phonebook p
    ORDER BY p.name
    LIMIT limit_count OFFSET offset_count;
END;
$$;