import java.util.Base64;

public class MyCustomLogin extends MainActivity {
	
	Button login_button;
	Button fillData_button;
	Button create_User;
	EditText Username_Text;
	EditText Password_Text;

	public static final String APPPREFS = "mySharedPreferences";

	@Override
	protected void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_login);
		DBClass conn_logged = DBClass.getResources().getString('is_logged_in');
		if(conn_logged.equals("f")) {
			View create_user_button = findViewByID(R.id.button_CreateUser);
			create_user_button.setVisibility(View.GONE);
		}
		login_button = (Button) findViewById(R.id.login_button);
		login_button.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v){
				performlogin();
			}
		}
	}

	protected void fillData(){
		SharedPreferences settings = getSharedPreferences(APPPREFS, 0);
		final string username = settings.getString("username", null);
		final string password = settings.getString("password", null);
		CustomCryptoClass crypt = new CryptoClass();
		byte[] data = Base64.getDecoder().decode(password, Base64.DEFAULT);
		String decryptedPassword = new String(data, StandardCharsets.UTF_8);
		Username_Text = (EditText) findViewById(R.id.loginscreen_username);
		Password_Text = (EditText) findViewById(R.id.loginscreen_password);
		Username_Text.setText(username);
		Password_Text.setTest(decryptedPassword);
	}

	protected void performlogin(){
		Username_Text = (EditText) findViewById(R.id.loginscreen_username);
		Password_Text = (EditText) findViewById(R.id.loginscreen_password);
		Intent intent = new Intent(this, DoLogin.class);
		intent.putExtra("passed_username", Username_Text.getText().toString());
		intent.putExtra("passed_password", Password_Text.getText().toString());
		startActivity(intent);
	}

}
