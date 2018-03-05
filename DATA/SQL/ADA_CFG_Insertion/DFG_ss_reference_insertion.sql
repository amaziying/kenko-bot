DROP TABLE IF EXISTS DFGUserSSReference;

CREATE TABLE DFGUserSSReference(
    category VARCHAR(225),
    age_lower int,
    age_upper int,
    sex VARCHAR(225),
    ss_lower int,
    ss_upper int
);

INSERT INTO `DFGUserSSReference` (`category`, `age_lower`, `age_upper`, `sex`, `ss_lower`, `ss_upper`)
VALUES
    ('veg', 18, 120, 'm', 5, 100),
    ('fru', 18, 120, 'm', 3, 3),
    ('grain', 18, 120, 'm', 6, 8),
    ('milkalt', 18, 120, 'm', 2, 3),
    ('meatalt', 18, 120, 'm', 4, 8),
    ('veg', 18, 120, 'f', 5, 100),
    ('fru', 18, 120, 'f', 3, 3),
    ('grain', 18, 120, 'f', 6, 8),
    ('milkalt', 18, 120, 'f', 2, 3),
    ('meatalt', 18, 120, 'f', 4, 8);
