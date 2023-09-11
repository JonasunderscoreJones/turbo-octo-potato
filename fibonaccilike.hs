chebyshev :: Int -> Int
chebyshev 0 = 0
chebyshev 1 = 2
chebyshev n = smartchebyshev 2 (n+1) 2 0

smartchebyshev :: Int -> Int -> Int -> Int -> Int
smartchebyshev curr max n1 n2
	| curr == max = n1
	| otherwise = smartchebyshev (curr + 1) max (4 * n1 - n2) n1