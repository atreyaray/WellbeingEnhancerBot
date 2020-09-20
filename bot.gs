var token = <token_here>;
var tgurl = "https://api.telegram.org/bot" + token;
var webAppUrl = <sheet_url_here>;

function setWebhook() {
  var url = tgurl + "/setWebhook?url=" + webAppUrl;
  var response = UrlFetchApp.fetch(url);
}

function sendMessage(chat_id, text, keyBoard) {
  var data = {
    method: "post",
    payload: {
      method: "sendMessage",
      chat_id: String(chat_id),
      text: text,
      parse_mode: "HTML",
      reply_markup: JSON.stringify(keyBoard)
    }
  };
  UrlFetchApp.fetch(tgurl + "/", data)
}

function doPost(e) {
  var contents = JSON.parse(e.postData.contents);
  var chat_id = contents.message.from.id; 
  var sender_id = contents.message.from.id;
  var first_name = contents.message.from.first_name;
  var last_name = contents.message.from.last_name;
  var received_text = contents.message.text;
  var response_text = "Hey " + first_name + ", you're working hard and doing a good job, keep it up!;)\n\n" + "For the list of commands just type help.";
  var date = new Date;
  
  var sheet_id = "1i8_1n1zKVQ-opH8O_cC4NwIoUfTYkjGiDu5DGyQln0Y";
  var sheet = SpreadsheetApp.openById(sheet_id).getSheetByName("Sheet1");
  var users = SpreadsheetApp.openById(sheet_id).getSheetByName("Sheet2");
  var split_text = received_text.split(" ");
  
  
  if(split_text[0] == "sleep") {
    sheet.appendRow([sender_id, first_name, last_name, received_text, date, split_text[1]]);
    var hours = split_text[1]
    var identifier = split_text[2]
    var totalhours = users.getDataRange().getCell((2 + Number(identifier)), 6).getValue();
    users.getDataRange().getCell((2 + Number(identifier)), 6).setValue(totalhours + Number(hours));
    var records = users.getDataRange().getCell((2 + Number(identifier)), 7).getValue();
    users.getDataRange().getCell((2 + Number(identifier)), 7).setValue(records + 1);
    var reaction = "";
    if(split_text[1] < 3) {
      reaction = "Poor you! That's so little sleep!😪"
    } else if(split_text[1] >= 3 && split_text[1] < 7) {
      reaction = "That's not enough sleep. Try to get some more tomorrow.😴"
    } else if(split_text[1] >= 7 && split_text[1] <= 9) {
      reaction = "Well done!🥳"
    } else if(split_text[1] > 9 ) {
      reaction = "Thats a lot of sleep... 😧"
    }
    
    var response = "sleep duration recorded. " + reaction 
    
    sendMessage(chat_id, response);
    
  } else if(split_text[0] == "/start") {
    var response = "Welcome to the bot! Here are the commands you can use: \n\n▫️'help' (will give you uthe list of commands)\n▫️'useful' (will give you useful sleep links)\n▫️'new' (creates a new user and responds with the user id) \n▫️'get y' (where y is your user id given to you when first creating your user. Give you your total sleep time) \n▫️'sleep x y' (where x is the number of hours you slept and where y is your user id given to you when first creating your user. Records a night’s sleep) \n▫️'average y' (Where y is your user id given to you when first creating your user. Gives you your averages sleep time) \n▫️'chart y' (Where y is your user id given to you when first creating your user. Gives you a chart comparing your average to recommended sleep) \n▫️'joke' (gives you a joke :)\n▫️'chill' (sends you some chill music)";
    sendMessage(chat_id,response);
    UrlFetchApp.fetch(tgurl + "/sendSticker?chat_id=" + chat_id + "&sticker=CAACAgIAAxkBAAIB719mcOrr7xeSMtxIHMww6TtxdVSHAAIPLwAC6VUFGMVYf-DuHYq4GwQ");
    
  }else if(split_text[0] == "new") {
    var id_counter = users.getDataRange().getCell(1,2).getValue();
    users.getRange('B1').setValue(id_counter + 1);
    users.appendRow([sender_id, first_name, last_name, received_text, date, 0, 0]);
    var response = "new user added succesfuly: your id is " + (id_counter+1);
    sendMessage(chat_id,response);
    
  } else if(split_text[0] == "get") {
    var identifier = split_text[1]
    var totalhours = users.getDataRange().getCell((2 + Number(identifier)), 6).getValue();
    var response = "your total sleep time: " + totalhours;
    sendMessage(chat_id,response);
    
  } else if(split_text[0] == "average") {
    var identifier = split_text[1]
    var totalhours = users.getDataRange().getCell((2 + Number(identifier)), 6).getValue();
    var records = users.getDataRange().getCell((2 + Number(identifier)), 7).getValue();
    var response = "your average sleep time: " + totalhours/records;
    sendMessage(chat_id,response);
    
  } else if(split_text[0] == "useful") {
    var response = "Here's some useful info on sleep health: \n" + "https://www.healthline.com/health/healthy-sleep#how-much-sleep-do-you-need?\n" + "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
    sendMessage(chat_id,response);
    
  } else if(split_text[0] == "chart") {
    var identifier = split_text[1]
    var userTotal = users.getDataRange().getCell((2 + Number(identifier)), 6).getValue();
    var user_first_name = users.getDataRange().getCell((2 + Number(identifier)), 2).getValue();
    var records = users.getDataRange().getCell((2 + Number(identifier)), 7).getValue();
    var userAverage = userTotal/records;
    var recommendedAverage = 8
    var response = "https://quickchart.io/chart?c={type:'bar',data:{datasets:[{label:'" + user_first_name + "',data:[" + userAverage + "]},{label:'Average',data:[" + recommendedAverage + "]}]}}";
    sendMessage(chat_id,response);
    
  } else if(split_text[0] == "help") {
    var response = "Would you like some help?\n" + "Here are the commands you can use: \n\n▫️'useful' (will give you useful sleep links)\n▫️'new' (creates a new user and responds with the user id) \n▫️'get y' (where y is your user id given to you when first creating your user. Give you your total sleep time) \n▫️'sleep x y' (where x is the number of hours you slept and where y is your user id given to you when first creating your user. Records a night’s sleep) \n▫️'average y' (Where y is your user id given to you when first creating your user. Gives you your averages sleep time) \n▫️'chart y' (Where y is your user id given to you when first creating your user. Gives you a chart comparing your average to recommended sleep) \n▫️'joke' (gives you a joke :)\n▫️'chill' (sends you some chill music)";
    sendMessage(chat_id,response);
    var rseponse_two ="For example create a user for yourself by typing 'new' and you will get your id. For example you got 3.\nThen you can type 'get 3' to see your sleep hours.\nOr you can type 'sleep 7 3' to record that you, the user with id 3, slept 7 hours."
    sendMessage(chat_id,rseponse_two);

  } else if(split_text[0] == "joke") {
    var joke = UrlFetchApp.fetch("https://sv443.net/jokeapi/v2/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist&format=txt&type=single").getContentText();
    sendMessage(chat_id,joke);
    
  } else if(split_text[0] == "sticker") {
    
    UrlFetchApp.fetch(tgurl + "/sendSticker?chat_id=" + chat_id + "&sticker=CAACAgIAAxkBAAIB719mcOrr7xeSMtxIHMww6TtxdVSHAAIPLwAC6VUFGMVYf-DuHYq4GwQ");
    
  } else if(split_text[0] == "chill") {
    
    var response = "Here are some beats for you to relax to 🐼: " + "https://www.youtube.com/watch?v=5qap5aO4i9A";
    sendMessage(chat_id,response);
    
  }else {
    
    sendMessage(chat_id,response_text);
    
  }
}