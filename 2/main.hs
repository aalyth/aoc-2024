
splitBy :: String -> Char ->  [String]
splitBy str delim =  case dropWhile (==delim) str of
    "" -> []
    s' -> w : splitBy  s'' delim
        where (w, s'') = break (==delim) s'


parseInput :: [String] -> [[Int]]
parseInput [] = []
parseInput lines = map (\line -> map read (splitBy line ' ')) lines

isRouteSafeInternal :: [Int] -> Bool -> Bool
isRouteSafeInternal [] _ = True
isRouteSafeInternal [_] _ = True
isRouteSafeInternal (x:y:xs) asc = 
        if asc 
           then (diff >= -3 && diff < 0) && isRouteSafeInternal (y:xs) asc
        else (diff > 0 && diff <= 3) && isRouteSafeInternal (y:xs) asc
        where 
                diff = x - y

isRouteSafe :: [Int] -> Bool
isRouteSafe [] = True
isRouteSafe [_] = True
isRouteSafe (x:y:xs) = isRouteSafeInternal (x:y:xs) (x < y)

removeAt :: [a] -> Int -> [a]
removeAt [] _ = []
removeAt (_:xs) 1 = xs
removeAt (x:xs) idx = x : removeAt xs (idx-1)

isRouteSafeWithTolerance :: [Int] -> Bool
isRouteSafeWithTolerance route = or [isRouteSafe (removeAt route idx) | idx <- [1..(length route)]]

getSafeRoutesCount :: [[Int]] -> Int
getSafeRoutesCount input = sum (map fromEnum routesSafety)
        where
                routesSafety = map isRouteSafeWithTolerance input

main :: IO()
main = do
        input <- readFile "./input.txt"
        let inputLines = lines input
        let input = parseInput inputLines
        print (getSafeRoutesCount input)
        putStrLn "hello"
