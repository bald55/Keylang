local x = 0
for i = 1, 300000000 do
    x = x + (i % 7)
end
print(x)
