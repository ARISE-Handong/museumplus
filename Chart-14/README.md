## Chart-14
- Bug information
	- Bug report: NA
	- Bug fix: https://github.com/jfree/jfreechart/commit/114ce73a5abb47971fcf059a8f18d829cbadea24
	- Bug type: Null pointer exception; Faulty program does not check null for the input variable
	- Fixed type: Omission fault
	- Fixed code: Check if input variable is null and handle the case
	- Snapshot of the fixed code:
		- 12 buggy lines (3 buggy lines for each bug)
		- Fault of the CategoryPlot@removeRangeMarker() is used for the experiment
		- source/org/jfree/chart/plot/CategoryPlot@removeDomainMarker(int, Marker, Layer, boolean)
		```diff
				markers = (ArrayList) this.backgroundDomainMarkers.get(new Integer(
        		            index));
        		}
       		+	if (markers == null) {
        	+		return false;
        	+	}
        		boolean removed = markers.remove(marker);
        		if (removed && notify) {
        		    fireChangeEvent();
		```
		- source/org/jfreechart/plot/CategoryPlot@removeRangeMarker(int, Marker, Layer, boolean)
		```diff
				else {
        		    markers = (ArrayList) this.backgroundRangeMarkers.get(new Integer(
        		            index));
        		}
        	+	if (markers == null) {
        	+		return false;
        	+	}
        		boolean removed = markers.remove(marker);
        		if (removed && notify) {
        		    fireChangeEvent();
		```
		- source/org/jfreechart/plot/XYPlot@removeDomainMarker(int, Marker, Layer, boolean)
		```diff
				else {
        		    markers = (ArrayList) this.backgroundDomainMarkers.get(
        		    		new Integer(index));
        		}
		+	if (markers == null) {
       		+		return false;
       		+	}
        		boolean removed = markers.remove(marker);
        		if (removed && notify) {
		```
		- source/org/jfreechart/plot/XYPlot@removeRangeMarker(int, Marker, Layer, boolean)
		```diff
				else {
        		    markers = (ArrayList) this.backgroundRangeMarkers.get(new Integer(
        		            index));
        		}
        	+	if (markers == null) {
        	+		return false;
        	+	}
        		boolean removed = markers.remove(marker);
        		if (removed && notify) {
        		    fireChangeEvent();
		```
- Failing test case
	- Testcase:
		- org.jfree.chart.plot.junit.CategoryPlotTests::testRemoveRangeMarker
		- org.jfree.chart.plot.junit.CategoryPlotTests::testRemoveDomainMarker
		- org.jfree.chart.plot.junit.XYPlotTests::testRemoveRangeMarker
		- org.jfree.chart.plot.junit.XYPlotTests::testRemoveDomainMarker
	- Target failing testcase:
		- org.jfree.chart.plot.junit.CategoryPlotTests::testRemoveRangeMarker
	- Stack trace: 
		- org.jfree.chart.plot.junit.CategoryPlotTests::testRemoveRangeMarker
			java.lang.NullPointerException
    		at org.jfree.chart.plot.CategoryPlot.removeRangeMarker(CategoryPlot.java:2448)
    		at org.jfree.chart.plot.CategoryPlot.removeRangeMarker(CategoryPlot.java:2415)
    		at org.jfree.chart.plot.CategoryPlot.removeRangeMarker(CategoryPlot.java:2396)
    		at org.jfree.chart.plot.CategoryPlot.removeRangeMarker(CategoryPlot.java:2378)
    		at org.jfree.chart.plot.junit.CategoryPlotTests.testRemoveRangeMarker(CategoryPlotTests.java:780)
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
		- org.jfree.chart.plot.junit.CategoryPlotTests::testRemoveDomainMarker
			java.lang.NullPointerException
    		at org.jfree.chart.plot.CategoryPlot.removeDomainMarker(CategoryPlot.java:2166)
    		at org.jfree.chart.plot.CategoryPlot.removeDomainMarker(CategoryPlot.java:2139)
    		at org.jfree.chart.plot.CategoryPlot.removeDomainMarker(CategoryPlot.java:2122)
    		at org.jfree.chart.plot.CategoryPlot.removeDomainMarker(CategoryPlot.java:2106)
    		at org.jfree.chart.plot.junit.CategoryPlotTests.testRemoveDomainMarker(CategoryPlotTests.java:771)
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
		- org.jfree.chart.plot.junit.XYPlotTests::testRemoveRangeMarker
			java.lang.NullPointerException
			at org.jfree.chart.plot.XYPlot.removeRangeMarker(XYPlot.java:2529)
    		at org.jfree.chart.plot.XYPlot.removeRangeMarker(XYPlot.java:2498)
    		at org.jfree.chart.plot.XYPlot.removeRangeMarker(XYPlot.java:2481)
    		at org.jfree.chart.plot.XYPlot.removeRangeMarker(XYPlot.java:2465)
    		at org.jfree.chart.plot.junit.XYPlotTests.testRemoveRangeMarker(XYPlotTests.java:1037)
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
		- org.jfree.chart.plot.junit.XYPlotsTests::testRemoveDomainMarker
			java.lang.NullPointerException
    		at org.jfree.chart.plot.XYPlot.removeDomainMarker(XYPlot.java:2293)
    		at org.jfree.chart.plot.XYPlot.removeDomainMarker(XYPlot.java:2265)
    		at org.jfree.chart.plot.XYPlot.removeDomainMarker(XYPlot.java:2248)
    		at org.jfree.chart.plot.XYPlot.removeDomainMarker(XYPlot.java:2232)
    		at org.jfree.chart.plot.junit.XYPlotTests.testRemoveDomainMarker(XYPlotTests.java:1028)
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
		- 386 lines of codes
	
- Test cases:
  - Total number of test cases: 1794 test cases
  - Target test cases: 978 test cases
    - 977 passing test cases
    - 1 failing test case
  - Test cases example
    - Passing test cases

    - Failing test cases
	  - org.jfree.chart.plot.junit.CategoryPlotTests::testRemoveRangeMarker
	  ```java
	  /**
       * Check that removing a marker that isn't assigned to the plot returns
       * false.
       */
      public void testRemoveRangeMarker() {
          CategoryPlot plot = new CategoryPlot();
          assertFalse(plot.removeRangeMarker(new ValueMarker(0.5)));
      }
	  ```

- Generated mutants:
  - Total 13758 mutants generated
  - 739 mutants generated on target statements
    - 5 mutants occur compile error
    - 734 mutants successfully executed
- Score
  - Dstar
    - Rank of the first buggy line: 4.5 at score 1.0
    - Top 5 ranks:
    	- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2448 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2415 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2442 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2440 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2396 -- 1.0
  - Ochiai
    - Rank of the first buggy line: 4.5 at score 0.7071067811865475
    - Top 5 ranks:
    	- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2442 -- 0.7071067811865475
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2440 -- 0.7071067811865475
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2415 -- 0.7071067811865475
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2441 -- 0.7071067811865475
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2396 -- 0.7071067811865475
  - Op2
    - Rank of the first buggy line: 4.5 at score 1.0
    - Top 5 ranks:
    	- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2448 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2442 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2440 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2378 -- 1.0
		- Rank 4.5: org/jfree/chart/plot/CategoryPlot.java#2436 -- 1.0
  - MUSE
    - Rank of the first buggy line: 1.5 at score 1.0
    - Top 5 ranks:
    	- Rank 1.5: org/jfree/chart/plot/CategoryPlot.java#2378 -- 1.0
		- Rank 1.5: org/jfree/chart/plot/CategoryPlot.java#2448 -- 1.0
		- Rank 3: org/jfree/chart/plot/CategoryPlot.java#2440 -- 0.6666666666666666
		- Rank 4: org/jfree/chart/plot/CategoryPlot.java#2239 -- 0.6664576428080863
		- Rank 159.5: org/jfree/chart/plot/PlotOrientation.java#72 -- 0
  - MUSEUM
    - Rank of the first buggy line: 1.5 at score 0.14285714285714285
    - Top 5 ranks:
    	- Rank 1.5: org/jfree/chart/plot/CategoryPlot.java#2378 -- 0.14285714285714285
		- Rank 1.5: org/jfree/chart/plot/CategoryPlot.java#2448 -- 0.14285714285714285
		- Rank 3: org/jfree/chart/plot/CategoryPlot.java#2440 -- 0.09523809523809523
		- Rank 4: org/jfree/chart/plot/CategoryPlot.java#2239 -- 0.09520803880714612
		- Rank 160: org/jfree/chart/plot/ValueMarker.java#68 -- 0
  - Metallaxis
    - Rank of the first buggy line: 4 at score 0.7071067811865475
    - Top 5 ranks:
    	- Rank 5: org/jfree/chart/plot/CategoryPlot.java#2442 -- 0.7071067811865475
		- Rank 5: org/jfree/chart/plot/CategoryPlot.java#2249 -- 0.7071067811865475
		- Rank 5: org/jfree/chart/plot/CategoryPlot.java#2239 -- 0.7071067811865475
		- Rank 5: org/jfree/chart/plot/CategoryPlot.java#2378 -- 0.7071067811865475
		- Rank 5: org/jfree/chart/plot/CategoryPlot.java#2448 -- 0.7071067811865475
  - Mutallaxis
  	- Rank of the first buggy line: 2.5 at score 1.0
	- Top 5 ranks:
		- Rank 2.5: org/jfree/chart/plot/CategoryPlot.java#2448 -- 1.0
		- Rank 2.5: org/jfree/chart/plot/CategoryPlot.java#2441 -- 1.0
		- Rank 2.5: org/jfree/chart/plot/CategoryPlot.java#2249 -- 1.0
		- Rank 2.5: org/jfree/chart/plot/CategoryPlot.java#2378 -- 1.0
		- Rank 5.5: org/jfree/chart/plot/CategoryPlot.java#2440 -- 0.6666666666666666

- Comparisons to the original result
  - Num of testcase

| Testcases   | Paper | New  |
| ----------- | ----- | -----|
| Target TCs  | 490  | 978 |
| Passing TCs | 486  | 977 |
| Failing TCs | 4   | 1 |


  - Num of target statements

|                   | Paper  | New   |
| ----------------- | ------ | ----- |
| Target statements | 6199    | 386   |

  - Generated Mutants

| Mutants        | Paper  | New   |
| -------------- | ------ | ----- |
| Total mutants  | 10880  | 13758 |
| Target mutants | 731   | 889  |

  - Ranks

| Techinuqes | Paper  | New     |
| ---------- | ------ | ------- |
| MUSE       | 5 |  1.5  |
| MUSEUM     |  |  1.5  |
| Metallaxis | 5 |  5  |
| Mutallaxis |  | 2.5 |
| Dstar      | 25.5 |  4.5  |
| Ochiai     | 15.5 |  4.5  |
| Op2        | 339.5 |  4.5  |
