#!/usr/bin/php

<?php

/*

This class is a part of the web application, which simulates a restricted shell. It can be run as a separate file.

*/


class TotalCommander{

	function __construct(){
		$this->run_command_line();
	}

	function display_logo(){
		$header = '___________     __         .__                                                    .___            
\__    ___/____/  |______  |  |     ____  ____   _____   _____ _____    ____    __| _/___________ 
  |    | /  _ \   __\__  \ |  |   _/ ___\/  _ \ /     \ /     \\__  \  /    \  / __ |/ __ \_  __ \
  |    |(  <_> )  |  / __ \|  |__ \  \__(  <_> )  Y Y  \  Y Y  \/ __ \|   |  \/ /_/ \  ___/|  | \/
  |____| \____/|__| (____  /____/  \___  >____/|__|_|  /__|_|  (____  /___|  /\____ |\___  >__|   
                         \/            \/            \/      \/     \/     \/      \/    \/       
' . PHP_EOL . PHP_EOL;
     	echo $header;
	}

	function display_menu(){
		echo str_repeat("-", 10);
		echo " M - E - N - U ";
		echo str_repeat("-", 10) . PHP_EOL;
		echo "1. Show this menu" . PHP_EOL;
		echo "2. List files in directory" . PHP_EOL;
		echo "3. Search text in log file" . PHP_EOL;
		echo "4. Launch interactive shell" . PHP_EOL;
		echo "5. Exit app" . PHP_EOL;
	}
	

	function check_menu_number($user_input){
		while(intval($user_input) < 1 || intval($user_input) > 5){
			echo "Wrong number, please provide one from 1-4." . PHP_EOL;
			$user_input = readline("Enter your choice: ");
		}
		return $user_input;
	}


	function run_command_line(){
		$this->display_logo();
		$this->display_menu();
		$user_input = readline("Enter your choice: ");
		$user_input = $this->check_menu_number(intval($user_input));
		while(intval($user_input) >= 1 && intval($user_input) <= 5){
			switch(intval($user_input)){
				case 1: $this->display_menu(); break;
				case 2: 
						$directory_location = readline("Provide directory path (/tmp is the base): "); 
						$this->list_files($directory_location);
					break;
				case 3: 
					$search_term = readline("Provide text you want to search for: ");
					$search_location = readline("Provide the logfile name to search in [under the /var/log/]: ");
					$this->log_text_search($search_term, $search_location);
					break;
				case 4: $this->function_not_exist(); break;
				case 5: $this->exit(); break;
			}
			$user_input = readline("Enter your choice: ");
			$this->check_menu_number(intval($user_input));
		}
	}

	function exit(){
		echo "Bye". PHP_EOL;
		die();
	}

	function function_not_exist(){
		echo "This function is currently not implemented." . PHP_EOL;
	}

	function list_files($directory_location, &$results = array()){
		$base = "/tmp/";
		$files = scandir($base . $directory_location);

		foreach($files as $key => $value){
			$path = realpath($base . $directory_location . DIRECTORY_SEPARATOR . $value);
			if(!is_dir($path)){
				$results[] = $path;
			} elseif($value != "." && $value != ".."){
				$this->list_files($path, $results);
				$results[] = $path;
			}
		}

		echo $directory_location . " contains: " . PHP_EOL;
		foreach($results as $result){
			echo $result . PHP_EOL;
		}
	}

	function log_text_search($string_to_search, $log_name){
		if(preg_match_all("/[\\'^£%&*(); \"@#~?\<>,|=]/", $log_name)){
			echo "Please provide a valid text! No special characters allowed! Exiting... " . PHP_EOL;
			exit();
		}
		if(preg_match_all("/[\\'^£$%&*() ;\"}{@#~?.\/<>,|=]/", $string_to_search)){
			echo "Please provide a valid text! No special characters allowed! Exiting... " . PHP_EOL;
			exit();
		}
		$log_name = str_replace("..", "", $log_name);
		$string_to_search = str_replace("..", "", $string_to_search);
		echo str_repeat("-", 10);
		echo PHP_EOL . "Searching for $string_to_search text in /var/log/$log_name" . PHP_EOL;
		echo str_repeat("-", 10);
		echo PHP_EOL;
		echo shell_exec("grep -i $string_to_search /var/log/$log_name");
	}
}


$totalCommander = new TotalCommander;
