# docker-compose-debizium-postgres

This is inspired by this article <https://www.startdataengineering.com/post/change-data-capture-using-debezium-kafka-and-pg/>

## Steps to run Debizium + consumer

### Step 1: Set up infra

```bash
./setup_infra.sh
```

### Step 2: Setup tables

```sql
CREATE SCHEMA bank;
SET search_path TO bank,public;
CREATE TABLE bank.holding (
    holding_id int,
    user_id int,
    holding_stock varchar(8),
    holding_quantity int,
    datetime_created timestamp,
    datetime_updated timestamp,
    primary key(holding_id)
);
ALTER TABLE bank.holding replica identity FULL;
insert into bank.holding values (1000, 1, 'VFIAX', 10, now(), now());
```

### Step 3: Add new connector

```bash
./add_connector.sh
```

### Step 4: Run consumer

```bash
docker run -it --rm --name consumer --link zookeeper:zookeeper \
--link kafka:kafka debezium/kafka:1.1 watch-topic \
-a bankserver1.bank.holding | grep --line-buffered '^{' \
| src/stream.py > output/holding_pivot.txt
```

### Step 5: Tail the logs

```bash
tail -f output/holding_pvt.txt
```

### Step 6: Add more operations to DB

```sql
-- C
insert into bank.holding values (1001, 2, 'SP500', 1, now(), now());
insert into bank.holding values (1002, 3, 'SP500', 1, now(), now());

-- U
update bank.holding set holding_quantity = 100 where holding_id=1000;

-- d
delete from bank.holding where user_id = 3;
delete from bank.holding where user_id = 2;

-- c
insert into bank.holding values (1003, 3, 'VTSAX', 100, now(), now());

-- u
update bank.holding set holding_quantity = 10 where holding_id=1003;
```

### Step 7: Tear down

```bash
./teardown.sh
```
