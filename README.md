# Data_Results_Creation
Coded using Python, the project is for the creation of statistical tests through a point-and-click system that allows users the ability to access given parameters (i.e. Data Columns) to allow the data to be taken into a testable format. The user is then allowed to select data to compare using statistical tests to be made into a data table.
There are a variety of issues that should be addressed regarding the Data Creation Version 1.0.
- Version 1.0 is the entirety of the process of taking data and converting it to a seperate data file of statistical results using a point-and-click system. Initially designed with only an International Monetary Fund (IMF) dataset in mind, the dataset is being remodeled to work for a variety of datasets. In its current form, the Data Creation file is meant for a file with a similar format to the IMF dataset (with a column of countries, a column of indicators, and a column of each year with its data, where the indicator columns have to be before any year in column order. At the same time, the parameters do not have to be countries, indicators, or years; they could be any set of 3 parameters that could be narrowed down, such as:
  > Subject, Treatment, Time
  
  > State, Category, Month
  
  > Weight, Initial Speed, Distance
- The current version requires a dataset that has a column of indicators before the separate year columns (preferably ordered), and with a country column. The new interface will not require that order (updates will have to be implemented).
- The current point-and-click system has a lot to be desired. It does not yet accomplish the goal of creating a dataset with statistical results. It also does not yet address the types of tests that I want it to run (right now, it only allows for one-sample T-tests, where the mean is expected to be a given country's indicator's year and either the aggregate of an indicator's specific year or the aggregate of an indicator as a whole are the choices of the data to compare it to.) Time series tests will have to be considered if the dataset allows/requires.
- The point-and-click system is supposed to have the ability to select the possible comparisons (i.e. the dataset of two countries given an indicator, the dataset of a given country indicator and that of another country's given indicator, etc,.). It also should have the decency to allow the ability to select the columns of the dataset (therefore, if one wants to select the indicator, country, and year columns, they should be able to, since not every dataset will be ordered, let alone with the parameters that are expected as columns.
- Test cases are very much in order. It will have to be very extensive and will ultimately have to be automated to run multiple datasets with multiple means of implementation.
- The current version has to be given more universal parameters and probably multiple processes to extract data from the dataset. The current process assumes that there is only one process which takes the data as if there has to be different columns per year, rather than a singular year column. Ideally, there would be a process that can choose between one or the other. The same problem is expected to be latent with all of the necessary parameters such that there may be different methods of selection. The current consideration is that there should be two files - one that takes multiple year columns and another that takes one year column - and one that selects the years alone, requiring that there be a total of three files. Another option is a module with a variety of functions that can be used contingent on given selections (selections that have yet to be added).
- The current version does not allow the user to select the file. It only allows the code to be edited to implement the necessary file (for now, the IMF dataset is the only dataset I have tested.) It also does not run unless the user replaces the 'data_file' with a file of their own that can run with the code through code editing. That is soon to change.
- Runtime efficiency is a concern. The current version relies heavily on for-loops and is clunkier than it should be (there are many lists, dictionaries, etc., that are likely unnecessary and the loops could potentially be replaced with recursive functions so long as that they greaten the efficiency of the program).
- The documentation of the code itself has to be heavily edited. Such edits will be made with time. While removing unnecessary items is a priority, it is particularly one important improvement to be made with the documentation of the program.
- Selections are made through a 'tkinter' graphical user interface (GUI). While there could be a different interface, it currently appears sufficient as well as ideal given the requirements. The project somewhat assumes that the user is knowledgeable enough on statistics to know that they are looking to statistically test given parameters, though they are not expected to know the deeper workings of programming and statistics; unless that assumption is ammended to assume a user with a higher level of statistical or programming knowledge, it will be important to be careful of how much there is to interpret given that the user should be able to work through the interface seamlessly enough to do so on their own (another separate version might be more based on the ability of the user to interpret with greater statistical and programming sophistication). It would also help to have an interface that is generally easier for the user to use.
# Note that the project only has one creator, so it takes time to make improvements.
