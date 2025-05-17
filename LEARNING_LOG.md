### What I learned Today
May 1 - 16, 2025
- How to setup HostedUI
    - Sign Up
    - Login
    - Callback Function
        - Explanation to each step in code comments
- Refresher on decorated functions
- Use python-jose for 'jwt' to decode token to use email and name

May 17, 2025
- Create a generate_fake_jwt() function in order to simulate logged in user
- JWT structure: <Header>.<Payload>.<Signature>
    - Convert to JSON, encode to bytes, Base64-URL-encoding it, Stripping the trailing =, Saving the result into header_b64
- Add an If statement in dashboard to use the fake jwt




### Debugging Notes




### TODO / Revisit later
