#-------------------------------------Load and clean data---------------------------------------------
#Loading and preliminery processing
income_edu <- read.csv("Income_edu.csv", header=T)
dimnames(income_edu) <- list(income_edu[,1], c(0,0.2,0.4,0.6,0.8))
income_edu <- income_edu[,2:ncol(income_edu)]
income_age <- read.csv("Income_age.csv", header=T)
dimnames(income_age) <- list(income_age[,1],c(0,0.2,0.4,0.6,0.8))
income_age <- income_age[,2:ncol(income_age)]
income_gender <- read.csv("Income_gender.csv", header=T)
income_gender <- income_gender[1:2, ]
dimnames(income_gender) <- list(income_gender[,1],c(0,0.2,0.4,0.6,0.8))
income_gender <- income_gender[,2:ncol(income_gender)]

#Converting factors to numeric
convert_factor_to_numeric <- function(data){
  for (i in 1:ncol(data)){
    data[,i] <- as.numeric(sub(',', '' , levels(data[,i])[data[,i]]))
  }
  return(data)
}
income_age <-convert_factor_to_numeric(income_age)
income_edu <- convert_factor_to_numeric(income_edu)
income_gender <- convert_factor_to_numeric(income_gender)

#Sample data and construct table for logistic regression
set.seed(1)
education <- rownames(income_edu)
education_data <- factor(t(sample(education, size=50, replace=T)), levels = education)
gender <- rownames(income_gender)
gender_data <- factor(t(sample(gender, size=50, replace=T)), levels = gender)
age <- rownames(income_age)
age_data <- factor(t(sample(age, size=50, replace=T)), levels = age)
income_level <- rnorm(n=50, mean = 500000, sd=200000)
data_table <- data.frame(gender_data, age_data, education_data, income_level)

#Assign response classification to table
generate_response_column <- function(data_table){
  response_column <- c()
  for (i in 1:nrow(data_table)){
    education_baseline <- as.numeric(income_edu[data_table[i,'education_data'],])
    gender_baseline <- as.numeric(income_gender[data_table[i,'gender_data'],])
    age_baseline <- as.numeric(income_age[data_table[i,'age_data'],])
    peer_education_income <- which.min(abs( education_baseline - data_table[i, 'income_level']))
    peer_gender_income <- which.min(abs(gender_baseline - data_table[i, 'income_level']))
    peer_age_income <- which.min(abs(age_baseline - data_table[i, 'income_level']))
    final_ranking <- mean(peer_age_income, peer_education_income, peer_gender_income)
    #For logistic regression------
    if (final_ranking > 2){
      response_column <- c(response_column, 1)
    }else {
      response_column <- c(response_column, 0)
    }

  }
  data_table <- data.frame(data_table, response_column)
  return(data_table)
}

#For logistic regression, assign response to data------
data_table <- generate_response_column(data_table)




#-------------------------------------Run regression---------------------------------------------
reg <- glm( response_column ~ gender_data+age_data+education_data+income_level, data=data_table, family= "binomial")
#read regression results
summary(reg)


#---------------------------------------Test regression------------------------------------------
test_logit <- function(reg){
  education_data <- factor(t(sample(education, size=5, replace=T)), levels = education)
  gender_data <- factor(t(sample(gender, size=5, replace=T)), levels = gender)
  age_data <- factor(t(sample(age, size=5, replace=T)), levels = age)
  income_level <- rnorm(n=5, mean = 300000, sd=100000)
  test_data_table <- data.frame(gender_data, age_data, education_data, income_level)
  response_vec <- round(predict(reg, newdata = test_data_table, type='response'))
  test_data_table <- data.frame(test_data_table, response_vec)
  return(test_data_table)
}

#------------------------------------Comparison----------------------------------------------------
user_comparison<- function(model_name){
  
  user_input<-function(message, upper_constraint){
    test <- as.numeric(readline(prompt=message))
    if (is.numeric(test) & (test <= upper_constraint)){
      return(as.integer(test))
    } else {
      print("ERROR: Please input a number in the specified range")
      test <- as.integer(readline(prompt=message))
      }
  }
  gender_data <- rownames(income_gender)[user_input("Please type '1' if you are a Male, '2' if you are a Female: ", upper_constraint= 2)]
  age_data <- rownames(income_age)[user_input("Type '1' if your age less than 30, '2' if between 30 to 34, '3' if between 35 to 39, '4' if 40 to 44, '5' if 45 to 54, '6' if 55 to 64, '7' if over 65: ", upper_constraint= 7)]
  education_data <- rownames(income_edu)[user_input("Type '1' if your education level is junior high, '2' if high school,'3' if high vocational highschool training,'4' if advanced vational training,'5' if undergraduate and above: ", upper_constraint= 5)]
  income_level <- user_input("Type in your yearly income level in Taiwanese Dollars: ", upper_constraint = Inf)
  test_data_table <- data.frame(gender_data = factor(gender_data), age_data=factor(age_data), education_data=factor(education_data), income_level)
  response_vec <- round(predict(model_name, newdata = test_data_table, type='response'))
  if (response_vec > 0){
    return("Your income is above average!")
  } else {
      return("Your income is average or below your peers...")
    }
}

user_comparison(reg)