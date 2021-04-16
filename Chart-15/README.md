## Chart-15
- Bug information
	- Bug report: NA
	- Bug fix: https://github.com/jfree/jfreechart/commit/4a6de2390d866a78e9ec5804f1cc7b805610b6b5
	- Bug type: Assertion error; Faulty program does not check null for the input variable
	- Fixed type: Omission fault
	- Fixed code: Check if input variable is null/not null and handle the case
	- Snapshot of the fixed code:
		- bug fixed in two parts of code
		- 6 buggy lines 
		- source/org/jfree/chart/plot/PiePlot@setExplodePercent(Comparable, double)
			- not executed by the failing test case
			- 2 buggy lines
		```diff
	    	public double getMaximumExplodePercent() {
        +		if (this.dataset == null) {
        +		    return 0.0;
        +		}
        		double result = 0.0;
        		Iterator iterator = this.dataset.getKeys().iterator();
        		while (iterator.hasNext()) {	
		```
		- source/org/jfree/chart/plot/PiePlot@initialise(Graphics2D, Rectangle2D, PiePlot, Integer, PlotRenderingInfo)
			- 4 buggy lines
		```diff
			PiePlotState state = new PiePlotState(info);
        	state.setPassesRequired(2);
        +	if (this.dataset != null) {
        	    state.setTotal(DatasetUtilities.calculatePieDatasetTotal(
        	            plot.getDataset()));
        +	}
        	state.setLatestAngle(plot.getStartAngle());
        	return state;
		```
- Failing test case
	- Testcase:
		- org.jfree.chart.plot.junit.PiePlot3DTests::testDrawWithNullDataset
	- Stack trace: 
		junit.framework.AssertionFailedError
    	at junit.framework.Assert.fail(Assert.java:55)
    	at junit.framework.Assert.assertTrue(Assert.java:22)
    	at junit.framework.Assert.assertTrue(Assert.java:31)
    	at junit.framework.TestCase.assertTrue(TestCase.java:201)
    	at org.jfree.chart.plot.junit.PiePlot3DTests.testDrawWithNullDataset(PiePlot3DTests.java:151)
    	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:57)
    	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    	at java.lang.reflect.Method.invoke(Method.java:606)
    	at junit.framework.TestCase.runTest(TestCase.java:176)
    	at junit.framework.TestCase.runBare(TestCase.java:141)
    	at junit.framework.TestResult$1.protect(TestResult.java:122)
    	at junit.framework.TestResult.runProtected(TestResult.java:142)
    	at junit.framework.TestResult.run(TestResult.java:125)
    	at junit.framework.TestCase.run(TestCase.java:129)
    	at junit.framework.TestSuite.runTest(TestSuite.java:255)
    	at junit.framework.TestSuite.run(TestSuite.java:250)
	- Target statements:
		- 1132 lines of codes
	
- Test cases:
  - Total number of test cases: 1787 test cases
  - Target test cases: 1054 test cases
    - 1053 passing test cases
    - 1 failing test case
  - Test cases example
    - Passing test cases

    - Failing test cases
	  - org.jfree.chart.plot.junit.PiePlot3DTests::testDrawWithNullDataset
	  ```java
	  /**
       * Draws a pie chart where the label generator returns null.
       */
      public void testDrawWithNullDataset() {
          JFreeChart chart = ChartFactory.createPieChart3D("Test", null, true,
                  false, false);
          boolean success = false;
          try {
              BufferedImage image = new BufferedImage(200 , 100,
                      BufferedImage.TYPE_INT_RGB);
              Graphics2D g2 = image.createGraphics();
              chart.draw(g2, new Rectangle2D.Double(0, 0, 200, 100), null, null);
              g2.dispose();
              success = true;
          }
          catch (Exception e) {
              success = false;
          }
          assertTrue(success);
    }
	```
- Generated mutants:
  - Total 27127 mutants generated
  - 2029 mutants generated on target statements
    - 4 mutants occur compile error
    - 2025 mutants successfully executed
- Score
  - Dstar
    - Rank of the first buggy line: 32 at score 0.333333333
    - Top 5 ranks:
    	- Rank 1.5: org/jfree/chart/plot/PiePlot.java#2613 -- 1.0
		- Rank 1.5: org/jfree/data/general/DatasetUtilities.java#153 -- 1.0
		- Rank 14.5: org/jfree/chart/plot/PiePlot.java#670 -- 0.5
		- Rank 14.5: org/jfree/chart/plot/PiePlot3D.java#248 -- 0.5
		- Rank 14.5: org/jfree/chart/plot/PiePlot3D.java#266 -- 0.5
  - Ochiai
    - Rank of the first buggy line: 32 at score 0.5
    - Top 5 ranks:
    	- Rank 1.5: org/jfree/chart/plot/PiePlot.java#2613 -- 0.7071067811865475
		- Rank 1.5: org/jfree/data/general/DatasetUtilities.java#153 -- 0.7071067811865475
		- Rank 14.5: org/jfree/chart/plot/PiePlot3D.java#247 -- 0.5773502691896258
		- Rank 14.5: org/jfree/chart/plot/PiePlot3D.java#242 -- 0.5773502691896258
		- Rank 14.5: org/jfree/chart/plot/PiePlot3D.java#251 -- 0.5773502691896258
  - Op2
    - Rank of the first buggy line: 32 at score 0.5
    - Top 5 ranks:
    	- Rank 1.5: org/jfree/data/general/DatasetUtilities.java#153 -- 1.0
		- Rank 1.5: org/jfree/chart/plot/PiePlot.java#2613 -- 1.0
		- Rank 14.5: org/jfree/chart/plot/PiePlot3D.java#248 -- 0.9990503323836657
		- Rank 14.5: org/jfree/chart/plot/PiePlot.java#1448 -- 0.9990503323836657
		- Rank 14.5: org/jfree/chart/plot/PiePlot3D.java#252 -- 0.9990503323836657
  - MUSE
    - Rank of the first buggy line: 230 at score 0
    - Top 5 ranks:
    	- Rank 1: org/jfree/chart/JFreeChart.java#1219 -- 0.9999663871195442
		- Rank 230: org/jfree/chart/util/HorizontalAlignment.java#65 -- 0
		- Rank 230: org/jfree/chart/ui/Library.java#82 -- 0
		- Rank 230: org/jfree/chart/ui/Library.java#129 -- 0
		- Rank 230: org/jfree/chart/title/LegendTitle.java#163 -- 0
  - MUSE
    - Rank of the first buggy line: 230 at score 0
    - Top 5 ranks:
    	- Rank 1: org/jfree/chart/JFreeChart.java#1219 -- 0.4999830163043478
		- Rank 230: org/jfree/chart/block/AbstractBlock.java#385 -- 0.0
		- Rank 230: org/jfree/chart/block/BlockContainer.java#241 -- 0.0
		- Rank 230: org/jfree/chart/text/TextLine.java#234 -- 0.0
		- Rank 230: org/jfree/chart/block/BlockBorder.java#167 -- 0.0
  - Metallaxis
    - Rank of the first buggy line: 706 at score 0
    - Top 5 ranks:
		- Rank 1: org/jfree/chart/JFreeChart.java#1219 -- 0.5773502691896258
		- Rank 2: org/jfree/chart/ChartFactory.java#694 -- 0.4082482904638631
		- Rank 3: org/jfree/chart/plot/PiePlot.java#494 -- 0.20851441405707477
		- Rank 4: org/jfree/chart/plot/Plot.java#519 -- 0.1643989873053573
		- Rank 6.5: org/jfree/chart/plot/PiePlot.java#401 -- 0.16222142113076254
  - Metallaxis
    - Rank of the first buggy line: 234.5 at score 0
    - Top 5 ranks:
		- Rank 234.5: org/jfree/chart/title/TextTitle.java#188 -- 0
		- Rank 234.5: org/jfree/chart/ChartColor.java#169 -- 0
		- Rank 234.5: org/jfree/chart/title/TextTitle.java#127 -- 0.0
		- Rank 234.5: org/jfree/chart/util/Size2D.java#73 -- 0
		- Rank 234.5: org/jfree/chart/plot/DefaultDrawingSupplier.java#101 -- 0
- Comparisons to the original result
  - Num of testcase

| Testcases   | Paper | New  |
| ----------- | ----- | -----|
| Target TCs  | 197   | 1054 |
| Passing TCs | 198   | 1053 |
| Failing TCs | 1     | 1 |


  - Num of target statements

|                   | Paper  | New   |
| ----------------- | ------ | ----- |
| Target statements | 11956  | 1132  |

  - Generated Mutants

| Mutants        | Paper  | New   |
| -------------- | ------ | ----- |
| Total mutants  | 21239   | 27127 |
| Target mutants | 1809    | 2029  |

  - Ranks

| Techinuqes | Paper  | New     |
| ---------- | ------ | ------- |
| MUSE       | 6333 |  230  |
| MUSEUM     |  |  230  |
| Metallaxis | 6452 |  706  |
| Mutallaxis |  | 234.5 |
| Dstar      | 34.5 |  32  |
| Ochiai     | 34.5 |  32  |
| Op2        | 34.5 |  32  |
