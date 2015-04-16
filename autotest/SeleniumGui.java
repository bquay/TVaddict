import javax.swing.*;
import javax.swing.text.BadLocationException;
import javax.swing.text.Style;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;
import java.awt.*;
import java.awt.event.ActionEvent;

/**
 * Created by Matt on 4/16/2015.
 */
public class SeleniumGui extends JFrame
{
   private static final String lineSep         = System.lineSeparator();
   private static final Color  bgColor         = new Color(60, 63, 65);
   private              Style  outputPaneStyle = null;

   private JTextPane outputPane;
   private JButton   startButton;

   private SeleniumGui()
   {
      super("Selenium Test GUI");
      setBackground(bgColor);
      setContentPane(createContentPane());
      setMinimumSize(new Dimension(300, 200));
      setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
      pack();
   }

   public Style getStyle()
   {
      if (outputPaneStyle == null)
      {
         outputPaneStyle = outputPane.addStyle("stylish", null);
      }

      return outputPaneStyle;
   }

   public void printLineToGui(String textToPrint)
   {
      printLineToGui(textToPrint, Color.WHITE);
   }

   public void printLineToGui(String textToPrint, Color textColor)
   {
      StyledDocument doc   = outputPane.getStyledDocument();
      Style          style = getStyle();

      StyleConstants.setForeground(style, textColor);
      StyleConstants.setBold(style, true);

      String textWithNewline;
      if (textToPrint.endsWith(lineSep))
      {
         textWithNewline = textToPrint;
      }
      else
      {
         textWithNewline = textToPrint + lineSep;
      }

      try
      {
         doc.insertString(doc.getLength(), textWithNewline, style);
      }
      catch (BadLocationException e)
      {
         e.printStackTrace();
      }
   }

   public void clearOutputPane()
   {
      outputPane.setText("");
   }

   private Container createContentPane()
   {
      JPanel contentPane = new JPanel();
      contentPane.setLayout(new GridBagLayout());
      contentPane.setBackground(bgColor);
      contentPane.setEnabled(true);
      startButton = new JButton();
      startButton.setAction(new StartSeleniumTestAction(this));
      startButton.setText("Start Selenium Test");
      startButton.setBackground(bgColor);
      startButton.setForeground(bgColor);
      GridBagConstraints gbc;
      gbc = new GridBagConstraints();
      gbc.gridx = 0;
      gbc.gridy = 0;
      gbc.weightx = 1.0;
      gbc.insets = new Insets(5, 5, 3, 5);
      contentPane.add(startButton, gbc);
      outputPane = new JTextPane();
      outputPane.setEditable(false);
      outputPane.setEnabled(true);
      outputPane.setOpaque(true);
      outputPane.setBackground(bgColor.brighter());
      outputPane.setText("");
      JScrollPane scrollPane = new JScrollPane(outputPane,
                                               ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED,
                                               ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED);
      gbc = new GridBagConstraints();
      gbc.gridx = 0;
      gbc.gridy = 1;
      gbc.weightx = 1.0;
      gbc.weighty = 1.0;
      gbc.fill = GridBagConstraints.BOTH;
      gbc.insets = new Insets(2, 5, 5, 5);
      contentPane.add(scrollPane, gbc);

      return contentPane;
   }

   private static class StartSeleniumTestAction extends AbstractAction
   {
      private final SeleniumGui gui;

      private StartSeleniumTestAction(SeleniumGui gui)
      {
         this.gui = gui;
      }

      @Override
      public void actionPerformed(ActionEvent e)
      {
         Object source = e.getSource();
         gui.clearOutputPane();
         ((JButton) source).setEnabled(false);
         gui.repaint();
         new Thread(new RunSeleniumTests(gui, (JButton) source)).start();
      }
   }

   protected static class RunSeleniumTests implements Runnable
   {
      private final JButton     button;
      private final SeleniumGui gui;

      public RunSeleniumTests(SeleniumGui gui, JButton toReenable)
      {
         this.gui = gui;
         this.button = toReenable;
      }

      @Override
      public void run()
      {
         Gmail.runTestsFromGUI(gui);
         SwingUtilities.invokeLater(() -> button.setEnabled(true));
      }
   }

   public static void main(String[] args)
   {
      try
      {
         // Set System L&F
         UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
      }
      catch (UnsupportedLookAndFeelException | ClassNotFoundException | IllegalAccessException | InstantiationException e)
      {
         // ignore
      }

      new SeleniumGui().setVisible(true); //Create and show the GUI.
   }
}
