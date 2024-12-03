
import Data.Map.Strict as HashMap

insertSorted :: Int -> [Int] -> [Int]
insertSorted x [] = [x]
insertSorted x (y:ys) = if y >= x then x:y:ys
                        else y : insertSorted x ys

splitBy :: String -> Char ->  [String]
splitBy str delim =  case dropWhile (==delim) str of
    "" -> []
    s' -> w : splitBy  s'' delim
        where (w, s'') = break (==delim) s'

parseLists :: [String] -> ([Int], [Int])
parseLists [] = ([], [])
parseLists lines = (insertSorted left leftList, insertSorted right rightList)
        where 
                currLine : linesRest = lines
                leftStr : rightStr : _ = splitBy currLine ' '
                left = read leftStr :: Int
                right = read rightStr :: Int
                (leftList, rightList) = parseLists linesRest
        
computeDistances :: [Int] -> [Int] -> Int
computeDistances [] [] = 0
computeDistances (x:xs) (y:ys) = abs (x - y) + computeDistances xs ys

rightInputToHashMap :: [Int] -> HashMap.Map Int Int
rightInputToHashMap [] = HashMap.empty
rightInputToHashMap (x:xs) = case HashMap.lookup x map of 
                Just occurances -> HashMap.insert x (occurances + 1) map
                Nothing -> HashMap.insert x 1 map
        where 
                map = rightInputToHashMap xs

computeSimilarity :: [Int] -> HashMap.Map Int Int -> Int
computeSimilarity [] _ = 0
computeSimilarity (x:xs) rightMap = case HashMap.lookup x rightMap of 
                Just occurances -> occurances * x + computeSimilarity xs rightMap 
                Nothing -> computeSimilarity xs rightMap

main :: IO()
main = do 
        input <- readFile "./input.txt"
        let inputLines = lines input
        let (left, right) = parseLists inputLines
        let rightMap = rightInputToHashMap right
        print rightMap
        print (computeDistances left right)
        print (computeSimilarity left rightMap)
        putStrLn "hello"
