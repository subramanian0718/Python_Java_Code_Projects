//Java Project:
//a program that repeatedly asks user for income and filing status and calculates the income tax. The program should stop if the user enters N for calculate another. 
//Use the single filers and married filing jointly table from https://www.nerdwallet.com/article/taxes/federal-income-tax-brackets to calculate the tax
//income tax is caculated using 2020 federal income tax brackets (for taxes due in April 2021, or in October 2021 with an extension)
import java.util.Scanner;
import java.math.BigDecimal;

//class which has main method
public class TaxCalculator {
    public static void main (String args[]) throws java.io.IOException {
        //variables that will be used for calculation are declared
        String filing_status= null;
        double income=0;                //used double data type as value can be large and can have values after decimal point
        double final_tax;   
        String calculate_another="Y";
        int rounded_final_tax;
        
        //start the while loop and continues until break is executed(ONLY when user enters "N")
        while(true){
            Scanner userInput = new Scanner(System.in);  // Create a Scanner object

            if(!calculate_another.equals("Y")){             //code to check whether another tax is to be calculated 
                System.out.println("Invalid input.Please enter Y or N to calculate another tax");
                System.out.println("Calculate another? (Y/N): ");       //check if we need to exit or continue
                calculate_another= userInput.nextLine();
                if(calculate_another.equals("N")){
                    break;
                }
                else if(!calculate_another.equals("Y")){
                    continue;
                }
            } 
            // String input
            if(income!=-1){                                 //enter filing status until correct value is entered
                System.out.println("Enter filing status: ");            
                filing_status = userInput.nextLine();
                if(!filing_status.equalsIgnoreCase("SINGLE") && !filing_status.equalsIgnoreCase("MARRIED")){         //check the filing status
                    System.out.println("Invalid input.Please enter correct filing status");
                    continue;
                }   
            }
            System.out.println("Enter Income: ");
            try {
                income= userInput.nextDouble();
                if( income<=0){                                    // check if value is lesser than OR equal to 0
                    System.out.println("Invalid input.Please ensure Income is greater than 0");     
                    income=-1;
                    continue;
                } 
            } catch (Exception e) {                             //catch exception if user enters value other than number 
                System.out.println("Invalid input.Please ensure Income is in digits.");
                income=-1;
                continue;
            }       
                
                final_tax=getTaxRate(filing_status,income);         //call the function
                if (final_tax % 1 == 0){                                         //code to display tax in integers alone if value after deciaml point is 0
                    rounded_final_tax = (int)Math.round(final_tax);   
                    System.out.println("Your tax due is $"+rounded_final_tax);                      
                }                                                                
                else{
                    System.out.println("Your tax due is $"+BigDecimal.valueOf(final_tax).toPlainString());      //code to display decimals if value after decimal point>0
                }
                //initialize all variables as they can be used again for checking conditions
                income=0;                           
                calculate_another="";
                System.out.println("Calculate another? (Y/N):");    //check if user wnats to caculate another tax
                calculate_another= userInput.next();
                if(calculate_another.equals("N")){
                    break;
                } 
          
        }
    }//main

    public static double getTaxRate(String filing_status,double income){        //function to find the rate of interest for user
        //initialize variables used in function
        double income_tax_total=0;
        int rate_of_tax=0;
        double min_tax_amount=0;
        double deductible_amount=0;
        if(filing_status.equalsIgnoreCase("SINGLE")){           //check for user when filing status is single
            if(income<=9875) {                                                 // #first bracket
                rate_of_tax=10;
            }           
            else if(income<=40125){                                            // #second bracket
                rate_of_tax=12;
                min_tax_amount=987.50;
                deductible_amount=9875;
            } 
            else if(income<=85525){                                                // #third bracket
                rate_of_tax=22;
                min_tax_amount=4617.50;
                deductible_amount=40125;
            }
            else if(income<=163300){                                              //#fourth bracket
                rate_of_tax=24;
                min_tax_amount=14605.50;
                deductible_amount=85525;
            }
            else if(income<=207350){                                               // #fifth bracket
                rate_of_tax=32;
                min_tax_amount=33271.50;
                deductible_amount=163300;
            } 
            else if(income<=518400){                                               // #sixth bracket
                rate_of_tax=35;
                min_tax_amount=47367.50;
                deductible_amount=207350;
            }
            else{                                                               //#last bracket
                rate_of_tax=37;
                min_tax_amount=156235;
                deductible_amount=518400;
            }

         }
         else if(filing_status.equalsIgnoreCase("MARRIED")){
            if(income<=19750) {                                                 // #first bracket
                rate_of_tax=10;
            }           
            else if(income<=80250){                                            // #second bracket
                rate_of_tax=12;
                min_tax_amount=1975;
                deductible_amount=19750;
            } 
            else if(income<=171050){                                                // #third bracket
                rate_of_tax=22;
                min_tax_amount=9235;
                deductible_amount=80250;
            }
            else if(income<=326600){                                              //#fourth bracket
                rate_of_tax=24;
                min_tax_amount=29211;
                deductible_amount=171050;
            }
            else if(income<=414700){                                               // #fifth bracket
                rate_of_tax=32;
                min_tax_amount=66543;
                deductible_amount=326600;
            } 
            else if(income<=622050){                                               // #sixth bracket
                rate_of_tax=35;
                min_tax_amount=94735;
                deductible_amount=414700;
            }
            else{                                                               //#last bracket
                rate_of_tax=37;
                min_tax_amount=167307.50;
                deductible_amount=622050;
            }

         }
         //call the function to return taxed income
         income_tax_total=getIncomeTax(filing_status,rate_of_tax,min_tax_amount,income,deductible_amount);
         return income_tax_total;       //return the value of income tax back to main part of program
    }

    //function to calculate tax using switch case
    public static double getIncomeTax(String filing_status, int tax_rate,double min_tax_amount,double income,double deductible_amount) {
        double income_tax_owed=0;
        try{
            switch(tax_rate) {
                case(10):                                       //check for the case of particular tax rate using switch case  
                income_tax_owed=((10D/100D)*(income));          //using "D" as we are using a double variable
                break;
                case(12):
                income_tax_owed=min_tax_amount+((12D/100D)*(income-deductible_amount));
                break;
                case(22):
                income_tax_owed=min_tax_amount+((22D/100D)*(income-deductible_amount)); 
                break;
                case(24):
                income_tax_owed=min_tax_amount+((24D/100D)*(income-deductible_amount));  
                break;
                case(32):
                income_tax_owed=min_tax_amount+((32D/100D)*(income-deductible_amount)); 
                break;
                case(35):
                income_tax_owed=min_tax_amount+((35D/100D)*(income-deductible_amount));
                break;
                case(37):
                income_tax_owed=min_tax_amount+((37D/100D)*(income-deductible_amount));
                break;
                                    
            }// switch case
            
        
        
    }catch (Exception exp) {        //catch exception in case of error during calculation and rerun program
        System.out.println("Following Error occurred during Income tax calculation.\n"+exp); 
        System.out.println("Please re-run the program.");     
        // Terminate JVM
        System.exit(0);
    }
        return income_tax_owed;     //return tax amount back to calling function
        
    } // getIncomeTax Method    

}
