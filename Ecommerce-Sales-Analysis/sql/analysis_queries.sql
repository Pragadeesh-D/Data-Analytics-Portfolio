-- Query 1 — Total Sales
SELECT SUM(Sales) AS Total_Sales
FROM orders;

-- Query 2 — Total Profit
SELECT SUM(Profit) AS Total_Profit
FROM orders;

-- Query 3 — Sales by Region
SELECT Region,
       SUM(Sales) AS Total_Sales
FROM orders
GROUP BY Region;

-- Query 4 — Monthly Sales Trend
SELECT Order_Year,
       Order_Month,
       SUM(Sales) AS Monthly_Sales
FROM orders
GROUP BY Order_Year, Order_Month
ORDER BY Order_Year;

-- Query 5 — Top 10 Products
SELECT Product_Name,
       SUM(Sales) AS Total_Sales
FROM orders
GROUP BY Product_Name
ORDER BY Total_Sales DESC
LIMIT 10;

-- Query 6 — Sales by Category
SELECT Category,
       SUM(Sales) AS Total_Sales
FROM orders
GROUP BY Category;

-- Query 7 — Customer Purchase Behavior
SELECT Customer_Name,
       COUNT(Order_ID) AS Total_Orders
FROM orders
GROUP BY Customer_Name
ORDER BY Total_Orders DESC
LIMIT 10;

-- Query 8 — Year-over-Year Sales Growth
SELECT Order_Year,
       SUM(Sales) AS Total_Sales,
       LAG(SUM(Sales)) OVER (ORDER BY Order_Year) AS Previous_Year_Sales,
       ((SUM(Sales) - LAG(SUM(Sales)) OVER (ORDER BY Order_Year)) / LAG(SUM(Sales)) OVER (ORDER BY Order_Year)) * 100 AS Growth_Percentage
FROM orders
GROUP BY Order_Year;

-- Query 9 — Profit Margin by Sub-Category
SELECT Sub_Category,
       SUM(Sales) AS Total_Sales,
       SUM(Profit) AS Total_Profit,
       (SUM(Profit) / SUM(Sales)) * 100 AS Profit_Margin
FROM orders
GROUP BY Sub_Category
ORDER BY Profit_Margin DESC;

-- Query 10 — Top 10 Profitable Customers
SELECT Customer_Name,
       SUM(Profit) AS Total_Profit
FROM orders
GROUP BY Customer_Name
ORDER BY Total_Profit DESC
LIMIT 10;

-- Query 11 — Average Shipping Delay by Ship Mode
SELECT Ship_Mode,
       AVG(DATEDIFF(STR_TO_DATE(Ship_Date, '%Y-%m-%d'), STR_TO_DATE(Order_Date, '%Y-%m-%d'))) AS Avg_Days_to_Ship
FROM orders
GROUP BY Ship_Mode;
