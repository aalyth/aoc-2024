import  Text.Regex.Posix

mulRegex = "mul\\([0-9]+,[0-9]+\\)"
advMulRegex = "(mul\\([0-9]+,[0-9]+\\))|(do\\(\\))|(don't\\(\\))"

splitBy :: String -> Char ->  [String]
splitBy str delim =  case dropWhile (==delim) str of
    "" -> []
    s' -> w : splitBy  s'' delim
        where (w, s'') = break (==delim) s'

-- removes the last element from the list
dropLast :: [a] -> [a]
dropLast [x] = []
dropLast (x:xs) = x : dropLast xs

parseMul :: String -> Int 
parseMul mulStr = left * right
        where 
                removedMulPrefix = drop 4 mulStr
                split = splitBy removedMulPrefix ','
                left = read (head split) :: Int
                right = read (dropLast (last split))

computeMultiples :: [String] -> Int
computeMultiples = foldr ((+) . parseMul) 0

computeMultiplesAdv :: [String] -> Bool -> Int
computeMultiplesAdv [] _ = 0
computeMultiplesAdv (x:xs) shouldCount = case x of 
        ('d':'o':'(':_) -> computeMultiplesAdv xs True
        ('d':'o':'n':_) -> computeMultiplesAdv xs False 
        _ -> if shouldCount 
                then parseMul x + computeMultiplesAdv xs True
             else computeMultiplesAdv xs False

main :: IO()
main = do
        input <- readFile "./input.txt"
        let inputLines = lines input
        let input = head inputLines
        let tmp = getAllTextMatches  (input =~ mulRegex) :: [String]
        let tmp2 = getAllTextMatches  (input =~ advMulRegex) :: [String]
        print (computeMultiples tmp)
        print (computeMultiplesAdv tmp2 True)
        putStrLn "hello"
