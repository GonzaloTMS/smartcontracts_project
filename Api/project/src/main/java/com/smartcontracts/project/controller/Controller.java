package com.smartcontracts.project.controller;

import java.math.BigInteger;
import java.util.Random;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.smartcontracts.project.model.RandomNumber;


@RestController
@RequestMapping("api")
public class Controller {

	
	@GetMapping("/random")
	public ResponseEntity<RandomNumber> getRandomNumber(){
		BigInteger random=new BigInteger(256,new Random()); 
		return new ResponseEntity<RandomNumber>(new RandomNumber(random), HttpStatus.OK);
	}
	
	

}
