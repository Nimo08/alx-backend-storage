-- Lists all bands with Glam rock as their main style, ranked by their longevity
SELECT
    band_name,
    DATEDIFF('2022-01-01', formed) AS lifespan
FROM metal_bands
WHERE
    style = 'Glam rock'
ORDER BY
    lifespan DESC;
