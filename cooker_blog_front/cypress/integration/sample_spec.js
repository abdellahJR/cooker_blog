describe('login works', () => {
  it('redirects to protected route', () => {
    cy.visit('http://localhost:3000/login');
    cy.get('.email').type('john1@snow.com');
    cy.get('.password').type('test');

    cy.get('.submit').click();

    cy.contains("id");
  });
});