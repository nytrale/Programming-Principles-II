-- 2. Insert or update a single user


CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS
$$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;



-- 3. Insert multiple users from arrays with validation


CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names VARCHAR[], 
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS
$$
DECLARE
    i INT;
    invalid_data TEXT := '';
BEGIN
    FOR i IN 1..array_length(p_names,1) LOOP
        -- must be digits only
        IF p_phones[i] ~ '^[0-9]+$' THEN
            CALL insert_or_update_user(p_names[i], p_phones[i]);
        ELSE
            invalid_data := invalid_data || p_names[i] || ':' || p_phones[i] || '; ';
        END IF;
    END LOOP;

    IF invalid_data <> '' THEN
        RAISE NOTICE 'Invalid: %', invalid_data;
    END IF;
END;
$$;



-- 5. Delete user by name or phone


CREATE OR REPLACE PROCEDURE delete_user(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS
$$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM phonebook WHERE name = p_name;
    END IF;
    IF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    END IF;
END;
$$;