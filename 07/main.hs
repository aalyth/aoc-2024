
import Debug.Trace

splitBy :: String -> Char ->  [String]
splitBy str delim =  case dropWhile (==delim) str of
    "" -> []
    s' -> w : splitBy  s'' delim
        where (w, s'') = break (==delim) s'


parseInput :: [String] -> [(Int, [Int])]
parseInput [] = []
parseInput (inp:tail) = (goal, nums) : parseInput tail
        where 
                goalRaw : numsRaw : _=  splitBy inp ':'
                goal = read goalRaw :: Int
                nums = [read num | num <- splitBy numsRaw ' ']


concatDigits :: Int -> Int -> Int
concatDigits x y = read (show x ++ show y) 

validEquationInner :: Int -> [Int] -> Int -> Bool
validEquationInner goal [] current = current == goal
validEquationInner goal (x:xs) current = multiplied || added || concated
      where 
                multiplied = validEquationInner goal xs (current * x)
                added = validEquationInner goal xs (current + x)
                concated = validEquationInner goal xs (concatDigits current x)


validEquation :: Int -> [Int] -> Bool
validEquation goal nums = validEquationInner goal nums 0

getCalibrationResult :: [(Int, [Int])] -> Int
getCalibrationResult []  = 0
getCalibrationResult ((goal, nums):rest) =
        if validEquation goal nums
           then goal + getCalibrationResult rest
        else getCalibrationResult rest 

main :: IO()
main = do
        input <- readFile "./input.txt"
        let inputLines = lines input
        let parsedInput = parseInput inputLines
        print (getCalibrationResult parsedInput)
        putStrLn "hello"
