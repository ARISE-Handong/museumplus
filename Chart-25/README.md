## Chart-25
- Bug information
	- The original buggy statements, failing test cases include 4 bugs
		- Not checking whether mean value is null in drawVerticalItem() (*used fault)
		- Not checking whether stddev is null in drawVerticalItem()
		- Not checking whether mean value is null in drawHorizontalItem()
		- Not checking whether stddev is null in drawHorizontalItem()
	- Bug report: NA
	- Bug fix: https://github.com/jfree/jfreechart/commit/3444dce49e30a4bcad864115d64d2c7656fc04a3
	- Bug type: Assertion failure; Buggy program does not check whether return value of a method is null before using it
	- Fixed type: Omission Fault
	- Fixed code: Added code that terminates the method when a value is null before using it
	- Snapshot of the fixed code:
		- 2 buggy lines
		- org/jfree/chart/renderer/category/StatisticalBarRenderer@drawVerticalItem(Graphics2D, CategoryItemRendererState, Rectangle2D, CategoryPlot, CategoryAxis, ValueAxis, int, int)
		```diff
		         // BAR X
		         Number meanValue = dataset.getMeanValue(row, column);
		+        if (meanValue == null) {
		+            return;
		+        }

		         double value = meanValue.doubleValue();
		         double base = 0.0;
		```
- Failing test case
	- All failing test cases:
		- org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests::testDrawWithNullMeanVertical
		- org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests::testDrawWithNullDeviationVertical
		- org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests::testDrawWithNullMeanHorizontal
		- org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests::testDrawWithNullDeviationHorizontal
	- Chosen failing test case:
		- org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests::testDrawWithNullMeanVertical
	- Stack trace:
		- org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests::testDrawWithNullMeanVertical
		junit.framework.AssertionFailedError
    		at junit.framework.Assert.fail(Assert.java:55)
    		at junit.framework.Assert.assertTrue(Assert.java:22)
    		at junit.framework.Assert.assertTrue(Assert.java:31)
    		at junit.framework.TestCase.assertTrue(TestCase.java:201)
    		at org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests.testDrawWithNullMeanVertical(StatisticalBarRendererTests.java:208)
	- Standard Error
		java.lang.NullPointerException
			at org.jfree.chart.renderer.category.StatisticalBarRenderer.drawVerticalItem(StatisticalBarRenderer.java:404)
			at org.jfree.chart.renderer.category.StatisticalBarRenderer.drawItem(StatisticalBarRenderer.java:212)
			at org.jfree.chart.plot.CategoryPlot.render(CategoryPlot.java:2868)
			at org.jfree.chart.plot.CategoryPlot.draw(CategoryPlot.java:2673)
			at org.jfree.chart.JFreeChart.draw(JFreeChart.java:1219)
	- Target statements:
		- 3172 lines of codes
	
- Test cases:
  - Total number of test cases: 1624 test cases
  - Target test cases: 1149 test cases
    - 1148 passing test cases
    - 1 failing test case
  - Test cases example
    - Passing test cases

    - Failing test cases
		- org.jfree.chart.renderer.category.junit.StatisticalBarRendererTests::testDrawWithNullMeanVertical
	```diff
    /**
     * Draws the chart with a <code>null</code> mean value to make sure that
     * no exceptions are thrown (particularly by code in the renderer).  See
     * bug report 1779941.
     */
    public void testDrawWithNullMeanVertical() {
        boolean success = false;
        try {
            DefaultStatisticalCategoryDataset dataset
                    = new DefaultStatisticalCategoryDataset();
            dataset.add(1.0, 2.0, "S1", "C1");
            dataset.add(null, new Double(4.0), "S1", "C2");
            CategoryPlot plot = new CategoryPlot(dataset,
                    new CategoryAxis("Category"), new NumberAxis("Value"),
                    new StatisticalBarRenderer());
            JFreeChart chart = new JFreeChart(plot);
            /* BufferedImage image = */ chart.createBufferedImage(300, 200,
                    null);
            success = true;
        }
        catch (NullPointerException e) {
            e.printStackTrace();
            success = false;
        }
        assertTrue(success);
    }
	```

- Generated mutants:
  - Total 24278 mutants generated
  - 6207 mutants generated on target statements
    - 48 mutants occur compile error
    - 6159 mutants successfully executed
- Score
  - Dstar
    - Rank of the first buggy line: 1809 at score 0
    - Top 5 ranks:
		- Rank 1809.5: org/jfree/chart/text/TextBlock.java#310 -- 0
		- Rank 1809.5: org/jfree/chart/plot/CategoryPlot.java#3047 -- 0
		- Rank 1809.5: org/jfree/chart/title/Title.java#197 -- 0
		- Rank 1809.5: org/jfree/chart/ui/BasicProjectInfo.java#150 -- 0
		- Rank 1809.5: org/jfree/chart/text/TextUtilities.java#714 -- 0
  - Ochiai
    - Rank of the first buggy line: 31.5 at score 0.5773502691896258
    - Top 5 ranks:
		- Rank 31.5: org/jfree/chart/renderer/category/StatisticalBarRenderer.java#211 -- 0.5773502691896258
		- Rank 31.5: org/jfree/chart/renderer/category/StatisticalBarRenderer.java#447 -- 0.5773502691896258
		- Rank 31.5: org/jfree/chart/renderer/category/StatisticalBarRenderer.java#485 -- 0.5773502691896258
		- Rank 31.5: org/jfree/chart/renderer/category/StatisticalBarRenderer.java#409 -- 0.5773502691896258
		- Rank 31.5: org/jfree/chart/renderer/category/StatisticalBarRenderer.java#419 -- 0.5773502691896258
  - Op2
    - Rank of the first buggy line: 1809.5 at score 1.0
    - Top 5 ranks:
		- Rank 1809.5: org/jfree/chart/axis/ValueAxis.java#586 -- 1
		- Rank 1809.5: org/jfree/chart/axis/CategoryAxis.java#747 -- 1
		- Rank 1809.5: org/jfree/chart/labels/ItemLabelAnchor.java#110 -- 1
		- Rank 1809.5: org/jfree/chart/plot/CategoryPlot.java#2616 -- 1
		- Rank 1809.5: org/jfree/chart/axis/ValueTick.java#103 -- 1
  - MUSE
    - Rank of the first buggy line: 1227 at score 0.0
	- Top 5 ranks
	  - Rank 20.5: org/jfree/data/KeyedObjects2D.java#239 -- 1.0
	  - Rank 20.5: org/jfree/data/KeyedObjects2D.java#236 -- 1.0
	  - Rank 20.5: org/jfree/data/statistics/DefaultStatisticalCategoryDataset.java#273 -- 1.0
	  - Rank 20.5: org/jfree/data/KeyedObjects2D.java#113 -- 1.0
	  - Rank 20.5: org/jfree/data/statistics/DefaultStatisticalCategoryDataset.java#111 -- 1.0
  - MUSEUM
    - Rank of the first buggy line: 1241 at score 0.0
	- Top 5 ranks
		- Rank 20.5: org/jfree/chart/plot/CategoryPlot.java#2862 -- 0.006329113924050633
		- Rank 20.5: org/jfree/data/statistics/DefaultStatisticalCategoryDataset.java#301 -- 0.006329113924050633
		- Rank 20.5: org/jfree/data/KeyedObjects2D.java#111 -- 0.006329113924050633
		- Rank 20.5: org/jfree/chart/plot/CategoryPlot.java#2868 -- 0.006329113924050633
		- Rank 20.5: org/jfree/data/statistics/DefaultStatisticalCategoryDataset.java#300 -- 0.006329113924050633
  - Metallaxis
    - Rank of the first buggy line: 849.5 at score 0.7071067811865475
    - Top 5 ranks:
        - Rank 884: org/jfree/chart/axis/NumberAxis.java#746 -- 0.7071067811865475
		- Rank 884: org/jfree/chart/renderer/category/AbstractCategoryItemRenderer.java#1022 -- 0.7071067811865475
		- Rank 884: org/jfree/chart/title/LegendTitle.java#442 -- 0.7071067811865475
		- Rank 884: org/jfree/chart/block/AbstractBlock.java#253 -- 0.7071067811865475
		- Rank 884: org/jfree/chart/util/RectangleInsets.java#437 -- 0.707106781186547

  - Mutallaxis
  	- Rank of the first buggy line: 638 at score 1.0
	- Top 5 ranks:
		- Rank 638: org/jfree/chart/axis/Tick.java#135 -- 1.0
		- Rank 638: org/jfree/chart/plot/CategoryPlot.java#2960 -- 1.0
		- Rank 638: org/jfree/chart/axis/NumberAxis.java#763 -- 1.0
		- Rank 638: org/jfree/chart/util/Layer.java#78 -- 1.0
		- Rank 638: org/jfree/chart/title/LegendTitle.java#438 -- 1.0

- Comparisons to the original result
  - Num of testcase

| Testcases   | Paper | New  |
| ----------- | ----- | -----|
| Target TCs  | 9  | 1149 |
| Passing TCs | 5   | 1148 |
| Failing TCs | 4    | 1 |

  - Num of target statements

|                   | Paper  | New   |
| ----------------- | ------ | ----- |
| Target statements | 10685   | 3172    |

  - Generated Mutants

| Mutants        | Paper  | New   |
| -------------- | ------ | ----- |
| Total mutants  | 18710   | 24278 |
| Target mutants | 5426    | 6207  |

  - Ranks

| Techinuqes | Paper  | New     |
| ---------- | ------ | ------- |
| MUSE       | 87 |  1227  |
| MUSEUM     |  |  1241  |
| Metallaxis | 457.5 |  849.5  |
| Mutallaxis |  | 638 |
| Dstar      | 2900.5 |  1809.5  |
| Ochiai     | 2792.5 |  31.5  |
| Op2        | 2900.5 |  1809.5  |
