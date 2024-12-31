# Solution explained

inside the Tests folder are the 4 provided problems resolved, each one inside their correspondence 

before most of the resolved problem (expect the angular app), you should install the requirements list in the `requirement.txt`

- ## Recursion and Colors
    the folder contains a single file called `custom_hanoi`, with it the disks can be changed as you please, it can be run with the command:
    ```sh
    python .\Tests\Recursion_Colors\custom_hanoi.py
    ``` 


- ## File Handling and Array operations
   the folder contains the FileProcessor class and a main.py file that allows to run all the requeste methods, run the program with the command:

   ```sh
    python .\Tests\File_Handling_Array_Operations\main.py
   ```

   The `read_dicom` method includes an option to save multi-frame DICOM files as a single image, by setting the `extract_with_mean` parameter to True.

- ## API Rest

   The folder contains a Django project that displays a REST API as requested 

   before running the app you should configure a .env file following the .env.example file, to provide the connection to the database.

   the database should be manually created before starting the app

   after that you can run the migrations to create the necesary tables so the application can run, with the command:

   ```sh
   python .\Tests\RESTfull_API\manage.py migrate
   ```

   after that you can run the app with the command:
   ```sh
   python .\Tests\RESTfull_API\manage.py runserver
   ```

   and API Rest will be accessible in http://localhost:8000/api/elements and ready to receive POST, GET, PUT and DELETE petitions

- ## Angular App

    to run the angular app, it would be best to get to it's folder with the command:

    ```sh
    cd .\Tests\angular_app\
    ```

    ### Install dependencies

    once here you can run the command:

    ```sh
    npm install
    ```

    to install all the depencies for the project.

    ### Run the project
    once everythin is install you can run the project with the command:

    ```sh
    npm start
    ```

    and the project will be available to see in the browser in http://localhost:4200
