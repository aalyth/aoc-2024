
import qualified Data.HashMap.Strict as HashMap
import qualified Data.HashSet as HashSet
import Data.Maybe (catMaybes, isNothing)
import Data.Hashable

splitBy :: String -> Char -> [String]
splitBy str delim =  case dropWhile (==delim) str of
    "" -> []
    s' -> w : splitBy  s'' delim
        where (w, s'') = break (==delim) s'

type PrefixMap k v = HashMap.HashMap k (HashSet.HashSet v)

prefixMapInsert :: (Eq k, Hashable k, Eq v, Hashable v) => k -> v -> PrefixMap k v -> PrefixMap k v 
prefixMapInsert key value map = case HashMap.lookup key map of
                Just bucket -> HashMap.insert key (HashSet.insert value bucket) map
                Nothing -> HashMap.insert key (HashSet.fromList [value]) map

prefixMapContains :: (Eq k, Hashable k, Eq v, Hashable v) => k -> v -> PrefixMap k v -> Bool
prefixMapContains key value map = case HashMap.lookup key map of 
                Just bucket -> HashSet.member value bucket
                Nothing -> False

buildPrefixMap :: [String] -> PrefixMap Int Int
buildPrefixMap ("":_) = HashMap.empty
buildPrefixMap (ln:lns) = prefixMapInsert (read after) (read before) map
        where 
                before : after : _ = splitBy ln '|'
                map = buildPrefixMap lns

validNextElement :: [Int] -> Int -> PrefixMap Int Int -> Bool
validNextElement [] _ _ = True
validNextElement (x:xs) el map = not (prefixMapContains x el map) && validNextElement xs el map

checkListOrderingInner :: [Int] -> [Int] -> PrefixMap Int Int -> Maybe Int
checkListOrderingInner traversed [] map = Just (getListMiddle traversed)
checkListOrderingInner traversed (x:xs) map = 
        if not (validNextElement traversed x map)
           then Nothing
        else checkListOrderingInner (x:traversed) xs map


checkListOrdering :: [Int] -> PrefixMap Int Int -> Maybe Int
checkListOrdering = checkListOrderingInner []


rawInputToSequences :: [String] -> [[Int]]
rawInputToSequences inp = [Prelude.map (\el -> read el :: Int) seq | seq <- sequencesSplit]
        where 
                secondInputHalf = tail (dropWhile (/= "") inp)
                sequencesSplit = Prelude.map (`splitBy` ',') secondInputHalf

computeSequenceOrdering :: [[Int]] -> PrefixMap Int Int -> Int
computeSequenceOrdering sequences map = sum (catMaybes checkedLists)
        where
                checkedLists = Prelude.map (`checkListOrdering` map) sequences


getListMiddle :: [ty] -> ty
getListMiddle list = list !! midIdx
        where 
                len = fromIntegral (length list)
                midIdx = floor (len/2)

sortInvalidSubsequence :: [Int] -> Int -> PrefixMap Int Int -> [Int]
sortInvalidSubsequence [] el _ = [el]
sortInvalidSubsequence (x:xs) el map = 
        if prefixMapContains x el map 
           then el : x : xs
        else x : sortInvalidSubsequence xs el map 

sortInvalidSequenceInner :: [Int] -> [Int] -> PrefixMap Int Int -> [Int]
sortInvalidSequenceInner traversed [] _ = traversed
sortInvalidSequenceInner traversed (x:xs) map = sortInvalidSequenceInner traversedSorted xs map
        where
                traversedSorted = sortInvalidSubsequence traversed x map


sortInvalidSequence :: [Int] -> PrefixMap Int Int -> [Int]
sortInvalidSequence = sortInvalidSequenceInner []

computeUnorderedSequences :: [[Int]] -> PrefixMap Int Int -> Int
computeUnorderedSequences [] map = 0
computeUnorderedSequences (seq:seqs) map =
        if isNothing (checkListOrdering seq map)
           then getListMiddle (sortInvalidSequence seq map) + subsequenceResult 
        else subsequenceResult
        where 
                subsequenceResult = computeUnorderedSequences seqs map

main :: IO()
main = do
        input <- readFile "./input.txt"
        let inputLines = lines input
        let map = buildPrefixMap inputLines
        let sequences = rawInputToSequences inputLines
        print (computeSequenceOrdering sequences map)
        print (computeUnorderedSequences sequences map)
        putStrLn "hello"
