import java.util.concurrent.TimeUnit;
import org.openqa.selenium.Alert;
import org.openqa.selenium.NoAlertPresentException;
import org.openqa.selenium.UnhandledAlertException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

public class Gmail
{
	private static WebDriver driver;
	private static String baseUrl;
	
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
		
		driver.close();
	}
	
	public static void ComposeMail(String username, String password, String sendTo, String subject) throws Exception
	{		
		/* Navigate to Gmail */
		driver.manage().timeouts().pageLoadTimeout(0, TimeUnit.MILLISECONDS);
		try
		{
			System.out.println("Navigating to start address");
			driver.get(baseUrl+"/intl/en/mail/help/about.html");
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
		String title = "Gmail";
		if (driver.getTitle().contains(title))
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
}