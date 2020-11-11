Feature: Login screen
  As a user,
  I want to see the Something prompt

  @Automation
  Scenario: App displays Login components
    Given the app displays the "Login" screen
    Then the app should display the "Username" field
    And the app should display the "Password" field
    And the app should display the "Login" button

  @Automation @valid_user
  Scenario: User can login in successfully
    Given the app displays the "Login" screen
    When the user types his credentials
    And the user taps on the "Login" button
    Then the app should display the "Home" screen

  @Automation @wip @valid_user
  Scenario: User view details of an item
    Given the app displays the "Home" screen
    # When the user taps on the "Login" button
    # Then the app should display the "Home" screen