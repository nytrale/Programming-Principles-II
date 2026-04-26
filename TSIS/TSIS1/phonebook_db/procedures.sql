
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
        RAISE NOTICE 'Контакт % обновлён', p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
        RAISE NOTICE 'Контакт % добавлен', p_name;
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i       INT;
    v_name  VARCHAR;
    v_phone VARCHAR;
BEGIN
    
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts (
        name  VARCHAR,
        phone VARCHAR,
        reason VARCHAR
    ) ON COMMIT DELETE ROWS;

    FOR i IN 1 .. array_length(p_names, 1) LOOP
        v_name  := p_names[i];
        v_phone := p_phones[i];

        IF v_phone !~ '^\+?[0-9\s\-]{7,20}$' THEN
            INSERT INTO invalid_contacts(name, phone, reason)
            VALUES (v_name, v_phone, 'Некорректный формат телефона');
        ELSE
            CALL upsert_contact(v_name, v_phone);
        END IF;
    END LOOP;
END;
$$;



CREATE OR REPLACE PROCEDURE delete_contact(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_username IS NOT NULL AND p_username <> '' THEN
        DELETE FROM contacts WHERE name ILIKE p_username;
        RAISE NOTICE 'Удалены контакты с именем: %', p_username;
    ELSIF p_phone IS NOT NULL AND p_phone <> '' THEN
        DELETE FROM contacts WHERE phone = p_phone;
        RAISE NOTICE 'Удалены контакты с телефоном: %', p_phone;
    ELSE
        RAISE NOTICE 'Укажи имя или телефон для удаления';
    END IF;
END;
$$;

-- procedures.sql — новые процедуры и функции для TSIS 1

-- 1. Добавить новый номер телефона к существующему контакту
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR  
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name ILIKE p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Контакт "%" не найден', p_contact_name;
        RETURN;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE NOTICE 'Неверный тип телефона: %. Используй: home, work, mobile', p_type;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);

    RAISE NOTICE 'Телефон % (%) добавлен контакту "%"', p_phone, p_type, p_contact_name;
END;
$$;


-- 2. Переместить контакт в другую группу (создать группу если не существует)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name ILIKE p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Контакт "%" не найден', p_contact_name;
        RETURN;
    END IF;

    -- Находим или создаём группу
    SELECT id INTO v_group_id
    FROM groups
    WHERE name ILIKE p_group_name
    LIMIT 1;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
        RAISE NOTICE 'Создана новая группа: "%"', p_group_name;
    END IF;

    -- Обновляем группу контакта
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;

    RAISE NOTICE 'Контакт "%" перемещён в группу "%"', p_contact_name, p_group_name;
END;
$$;


-- 3. Расширенный поиск — по имени, email и всем телефонам из таблицы phones
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id       INT,
    name     VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR,
    phone    VARCHAR,
    type     VARCHAR
) AS $$
BEGIN
    RETURN QUERY
        SELECT DISTINCT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name      AS grp,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE
            c.name  ILIKE '%' || p_query || '%'
         OR c.email ILIKE '%' || p_query || '%'
         OR p.phone ILIKE '%' || p_query || '%'
        ORDER BY c.name;
END;
$$ LANGUAGE plpgsql;