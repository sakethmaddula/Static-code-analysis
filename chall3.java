private class WebViewActivity extends MainActivity {
	
	@Overrride
	public void onCreate(Bundle savedInstanceState){
		super.onCreate(savedInstanceState);
		setContentView(R.layout.webview);
		mEdit   = (EditText)findViewByID(R.id.edittext);
		mButton = (Button)findViewByID(R.id.button);
		String mUrl = getIntent().getStringExtra("DEFAULT_URL");
		mButton.setOnClickListener(
			new View.OnClickListener(){
				public void onClick(View view){
					mUrl = mEdit.getText().toString();
				}
			}
			);
		if (mWebView == null){
			
			mWebView = new WebView(getActivity().getApplicationContext());
			mWebView.setFocusable(true);
			mWebView.setFocusableInTouchMode(true);
			mWebView.setClickable(true);

			WebSettings webSettings = mWebView.getSettings();

			CookieManager cookieManager = CookieManager.getInstance();
			cookieManager.setAcceptCookie(true);
			cookieManager.removeAllCookie();

			mwebView.setWebViewClient(new WebViewClient(){
				@Override
				public void onPageFinished(WebView view, String url){
					super.onPageFinished(view, url);
					webView.loadUrl(mUrl)
				}
			});
		}
	}

	@Override
	public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error){
		handler.proceed();
	}

}
