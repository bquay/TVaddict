import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.NoAlertPresentException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.UnhandledAlertException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.awt.*;
import java.util.concurrent.TimeUnit;

public class Gmail
{
   private static WebDriver driver;
   private static String    baseUrl;
   private static String[] wordsForIndexes = {"1st", "2nd", "3rd"};

   public static void main(String[] args) throws Exception
   {
      System.out.println("Opening Firefox...");
      driver = new FirefoxDriver();
      baseUrl = "https://gmail.com";
      driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
      // driver.manage().window().maximize();

      String[] username = new String[4];
      String[] password = new String[4];

      username[0] = "trendanalyzertest1@gmail.com";
      username[1] = "trendanalyzertest2@gmail.com";
      username[2] = "trendanalyzertest3@gmail.com";
      username[3] = "trendanalyzertest4@gmail.com";

      password[0] = "trendAnalyzer";
      password[1] = "trendAnalyzer";
      password[2] = "analyzeTrends";
      password[3] = "1234512345dd";

      String sendTo = "vote@pittdesignexpo.appspotmail.com";

      try
      {
         for (int i = 0; i < 4; i++)
         {
            ComposeMail(username[i], password[i], sendTo, Integer.toString(i + 1));
         }
      }
      catch (Exception e)
      {
         e.printStackTrace();
      }

   }

   public static void runTestsFromGUI(SeleniumGui gui)
   {
      System.out.println("Opening Firefox...");
      driver = new FirefoxDriver();
      baseUrl = "https://gmail.com";
      driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
      // driver.manage().window().maximize();

      String[] username = new String[4];
      String[] password = new String[4];

      username[0] = "trendanalyzertest1@gmail.com";
      username[1] = "trendanalyzertest2@gmail.com";
      username[2] = "trendanalyzertest3@gmail.com";
      username[3] = "trendanalyzertest4@gmail.com";

      password[0] = "trendAnalyzer";
      password[1] = "trendAnalyzer";
      password[2] = "analyzeTrends";
      password[3] = "1234512345dd";

      String sendTo = "vote@pittdesignexpo.appspotmail.com";

      Exception storedException = null;
      try
      {
         prepare();

         for (int i = 0; i < 4; i++)
         {
            ComposeMail(username[i], password[i], sendTo, Integer.toString(i + 1));
         }

         long timeOfLastSend = System.currentTimeMillis();

         postpare();

         long timePassed = System.currentTimeMillis() - timeOfLastSend;
         long timeToWait = (1000 * 61) - timePassed;

         // rounds timeToWait to the closest multiple of 1000 that is greater than timeToWait, then divides by 1000
         //  to get seconds
         long secondsToWait = ((timeToWait - (timeToWait % 1000)) + 1000) / 1000;
         System.out.println("Waiting for " + secondsToWait + " seconds to make sure trend-checking cronjob has run");
         System.out.print("Seconds left: " + secondsToWait + "...");
         while (timeToWait > (10 * 1000))
         {
            Thread.sleep(10 * 1000);
            timeToWait -= (10 * 1000);
            secondsToWait = ((timeToWait - (timeToWait % 1000)) + 1000) / 1000;
            System.out.print(secondsToWait + "...");
         }
		 System.out.print("\n");

         checkResults(gui);
      }
      catch (Exception e)
      {
         e.printStackTrace();
         storedException = e;
      }

      if (storedException != null)
      {
         gui.printLineToGui("An exception occurred while running the automated tests!", Color.RED.brighter());
         gui.printLineToGui(storedException.toString(), Color.RED.brighter());
      }
   }

   private static void postpare()
   {
//      System.out.println("Stopping voting...");
//      driver.get("http://pittdesignexpo.appspot.com/stopVoting");
//
//      if (!driver.findElement(By.xpath("//h1[@id='stopVote']")).isDisplayed())
//      {
//
//         System.out.println("Waiting for the login info fields to be visible");
//         waitForVisibleByXpath("//input[@id='Passwd']");
//
//         if (!driver.findElement(By.xpath("//input[@id='Email']")).isDisplayed())
//         {
//            System.out.println("Clicking the \"X\" to sign out");
//            driver.findElement(By.xpath("//div[@id='remove-link']")).click();
////
////         System.out.println("Waiting for the add account link to be visible");
////         waitForVisibleByXpath("//a[@id='account-chooser-add-account']");
////         System.out.println("Clicking the \"Add account\" link");
////         driver.findElement(By.xpath("//a[@id='account-chooser-add-account']")).click();
//         }
//
//         System.out.println("Waiting for the login info fields to be visible");
//         waitForVisibleByXpath("//input[@id='Email']");
//         System.out.println("Entering \"trendanalyzertest1@gmail.com\" as the account name");
//         driver.findElement(By.xpath("//input[@id='Email']")).clear();
//         driver.findElement(By.xpath("//input[@id='Email']")).sendKeys("trendanalyzertest1@gmail.com");
//         System.out.println("Entering \"trendAnalyzer\" as the password");
//         driver.findElement(By.xpath("//input[@id='Passwd']")).clear();
//         driver.findElement(By.xpath("//input[@id='Passwd']")).sendKeys("trendAnalyzer");
//         driver.findElement(By.xpath("//input[@id='signIn']")).click();
//
//         System.out.println("Waiting for voting stopped page to finish loading");
//         waitForPresenceByXpath("//h1[@id='stopVote']");
//
//      }
//
//      System.out.println("Logging out");
//      driver.get("https://accounts.google.com/logout");
//      System.out.println("Waiting for the \"X\" used to log out to be visible");
//      waitForVisibleByXpath("//div[@id='remove-link']");
//      System.out.println("Clicking the \"X\" to sign out");
//      driver.findElement(By.xpath("//div[@id='remove-link']")).click();
//      System.out.println("Waiting for the login info fields to be visible to confirm logout");
//      waitForVisibleByXpath("//input[@id='Email']");

      driver.get("http://pittdesignexpo.appspot.com/results");
   }

   public static void prepare()
   {
      System.out.println("Stopping voting...");
      driver.get("http://pittdesignexpo.appspot.com/stopVoting");

      System.out.println("Waiting for the login info fields to be visible");
      waitForVisibleByXpath("//input[@id='Passwd']");

      if (!driver.findElement(By.xpath("//input[@id='Email']")).isDisplayed())
      {
         System.out.println("Clicking the \"X\" to sign out");
         driver.findElement(By.xpath("//div[@id='remove-link']")).click();

//         System.out.println("Clicking the \"Sign in with a different account\" link");
//         driver.findElement(By.xpath("//a[@id='account-chooser-link']")).click();
//
//         System.out.println("Waiting for the add account link to be visible");
//         waitForVisibleByXpath("//a[@id='account-chooser-add-account']");
//         System.out.println("Clicking the \"Add account\" link");
//         driver.findElement(By.xpath("//a[@id='account-chooser-add-account']")).click();
      }

      System.out.println("Waiting for the login info fields to be visible");
      waitForVisibleByXpath("//input[@id='Email']");
      System.out.println("Entering \"trendanalyzertest1@gmail.com\" as the account name");
      driver.findElement(By.xpath("//input[@id='Email']")).clear();
      driver.findElement(By.xpath("//input[@id='Email']")).sendKeys("trendanalyzertest1@gmail.com");
      System.out.println("Entering \"trendAnalyzer\" as the password");
      driver.findElement(By.xpath("//input[@id='Passwd']")).clear();
      driver.findElement(By.xpath("//input[@id='Passwd']")).sendKeys("trendAnalyzer");
      driver.findElement(By.xpath("//input[@id='signIn']")).click();

      System.out.println("Waiting for voting stopped page to finish loading");
      waitForPresenceByXpath("//h1[@id='stopVote']");

      System.out.println("Clearing the DB");
      driver.get("http://pittdesignexpo.appspot.com/clearDB");
      System.out.println("Waiting for clear DB page to finish loading");
      waitForPresenceByXpath("//h1[@id='clearDB']");

      System.out.println("Adding posters");
      driver.get("http://pittdesignexpo.appspot.com/addPosters");
      System.out.println("Waiting for add posters page to finish loading");
      waitForPresenceByXpath("//h1[@id='addPosters']");

      System.out.println("Restarting voting");
      driver.get("http://pittdesignexpo.appspot.com/startVoting");
      System.out.println("Waiting for voting started page to finish loading");
      waitForPresenceByXpath("//h1[@id='startVote']");
	  
	   System.out.println("Logging out");
      driver.get("https://accounts.google.com/logout");
      System.out.println("Waiting for the \"X\" used to log out to be visible");
      waitForVisibleByXpath("//div[@id='remove-link']");
      System.out.println("Clicking the \"X\" to sign out");
      driver.findElement(By.xpath("//div[@id='remove-link']")).click();
      System.out.println("Waiting for the login info fields to be visible to confirm logout");
      waitForVisibleByXpath("//input[@id='Email']");
   }

   public static void ComposeMail(String username, String password, String sendTo, String subject) throws Exception
   {
      /* Navigate to Gmail */
      driver.manage().timeouts().pageLoadTimeout(0, TimeUnit.MILLISECONDS);
      try
      {
         System.out.println("Navigating to start address");
         driver.get(baseUrl + "/intl/en/mail/help/about.html");
      }
      catch (TimeoutException ignored)
      {
         // expected, ok
      }

      if (isDialogPresent(driver))
      {
         try
         {
            System.out.println("Accepting alert");
            Alert alert = driver.switchTo().alert();
            alert.accept();
            driver.switchTo().defaultContent();
         }
         catch (NoAlertPresentException ignored)
         {
            // do nothing
         }
      }

      // wait for "https://gmail.com/intl/en/mail/help/about.html" to load
      System.out.println("Waiting for sign-in link to be clickable");
      waitForVisibleByXpath("//a[@id='gmail-sign-in']");

      driver.manage().timeouts().pageLoadTimeout(20, TimeUnit.SECONDS);

		/* Enter username and password */
      System.out.println("Clicking the \"Sign in\" link");
      driver.findElement(By.xpath("//a[@id='gmail-sign-in']")).click();

      System.out.println("Waiting for the login info fields to be visible");
      waitForVisibleByXpath("//input[@id='Passwd']");

      if (!driver.findElement(By.xpath("//input[@id='Email']")).isDisplayed())
      {
         System.out.println("Clicking the \"Sign in with a different account\" link");
         driver.findElement(By.xpath("//a[@id='account-chooser-link']")).click();

         System.out.println("Waiting for the add account link to be visible");
         waitForVisibleByXpath("//a[@id='account-chooser-add-account']");
         System.out.println("Clicking the \"Add account\" link");
         driver.findElement(By.xpath("//a[@id='account-chooser-add-account']")).click();
      }

      System.out.println("Waiting for the login info fields to be visible");
      waitForVisibleByXpath("//input[@id='Email']");
      System.out.println("Entering \"" + username + "\" as the account name");
      driver.findElement(By.xpath("//input[@id='Email']")).clear();
      driver.findElement(By.xpath("//input[@id='Email']")).sendKeys(username);
      System.out.println("Entering \"" + password + "\" as the password");
      driver.findElement(By.xpath("//input[@id='Passwd']")).clear();
      driver.findElement(By.xpath("//input[@id='Passwd']")).sendKeys(password);
      driver.findElement(By.xpath("//input[@id='signIn']")).click();

		/*Verify login */
      if (driver.getTitle().contains("Gmail"))
      {
         System.out.println("Logged in successfully!!! " + driver.getTitle());
      }
      else
      {
         System.out.println("Unable to log in :-( " + driver.getTitle());
      }

		/* Compose email */
      System.out.println("Waiting for the compose button to be visible");
      waitForVisibleByXpath("//div[contains(text(),'COMPOSE')]");
      System.out.println("Clicking the compose button");
      driver.findElement(By.xpath("//div[contains(text(),'COMPOSE')]")).click();

		/* Enter email details */
      System.out.println("Waiting for the email \"To:\" field to be visible");
      waitForVisibleByXpath("//textarea[@name='to']");
      System.out.println("Entering \"" + sendTo + "\" as the To address");
      driver.findElement(By.xpath("//textarea[@name='to']")).sendKeys(sendTo);
      System.out.println("Entering \"" + subject + "\" as the subject");
      driver.findElement(By.xpath("//input[@placeholder='Subject']")).sendKeys(subject);
      System.out.println("Clicking the send button");
      driver.findElement(By.xpath("//div[text()='Send']")).click();

      System.out.println("Waiting for the \"Your message has been sent\" message to appear");
      waitForVisibleByXpath("//div[contains(text(),'Your message has been sent')]");

      System.out.println("Logging out");
      driver.get("https://accounts.google.com/logout");
      System.out.println("Waiting for the \"X\" used to log out to be visible");
      waitForVisibleByXpath("//div[@id='remove-link']");
      System.out.println("Clicking the \"X\" to sign out");
      driver.findElement(By.xpath("//div[@id='remove-link']")).click();
      System.out.println("Waiting for the login info fields to be visible to confirm logout");
      waitForVisibleByXpath("//input[@id='Email']");
   }

   private static void checkResults(SeleniumGui gui)
   {
      assert (driver.getCurrentUrl().equals("http://pittdesignexpo.appspot.com/results"));
      System.out.println("Refreshing results page");
      driver.navigate().refresh();

      // ensure that the tags are visible
      waitForVisibleByXpath("//table[@id='trendTable']");

      // get all values
      String[] expectedTags   = {"robots", "cs", "software"};
      String[] expectedCounts = {"3", "2", "2"};
      boolean allExpected = true;
	  System.out.println("Getting and checking all trend tags and counts");
      for (int i = 1; i <= 3; i++)
      {
         String observedTag = driver.findElement(By.xpath("//td[@id='trend" + i + "']")).getText();
         String observedCount = driver.findElement(By.xpath("//td[@id='count" + i + "']")).getText();
         allExpected &= checkValue(gui, "tag", (i - 1), expectedTags[i - 1], observedTag);
         allExpected &= checkValue(gui, "count", (i - 1), expectedCounts[i - 1], observedCount);
      }

      if (allExpected)
      {
         gui.printLineToGui("All values were as expected!");
		 System.out.println("All values were as expected!");
      }
      else
      {
         gui.printLineToGui("Some values were not as expected!", Color.RED.brighter());
		 System.out.println("Some values were not as expected!");
      }
   }

   private static boolean checkValue(SeleniumGui gui,
                                  String valueType,
                                  int valueIndex,
                                  String expectedValue,
                                  String observedValue)
   {

      if (expectedValue.equals(observedValue))
      {
         gui.printLineToGui("The " + wordsForIndexes[valueIndex] + " " + valueType
                                  + " (\"" + observedValue + "\") is the expected value.");
         return true;
      }
      else
      {
         gui.printLineToGui("The " + wordsForIndexes[valueIndex] + " " + valueType
                                  + " (\"" + observedValue + "\") is NOT the expected value, which is \""
                                  + expectedValue + "\"",
                            Color.RED.brighter());
         return false;
      }
   }


   private static boolean isDialogPresent(WebDriver driver)
   {
      try
      {
         System.out.print("Checking if alert is present: ");
         driver.getTitle();
         System.out.print("NOT PRESENT\n");
         return false;
      }
      catch (UnhandledAlertException e)
      {
         // Modal dialog showed
         System.out.print("PRESENT\n");
         return true;
      }
   }

   private static void waitForVisibleByXpath(String Xpath)
   {
      WebDriverWait wait = new WebDriverWait(driver, 10);
      wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath(Xpath)));
   }

   private static void waitForPresenceByXpath(String Xpath)
   {
      WebDriverWait wait = new WebDriverWait(driver, 10);
      wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(Xpath)));
   }
}
