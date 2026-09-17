/// <reference types="cypress" />


describe('1601', function () {
    var homeurl = 'https://example.internal/'
    var gameurl = 'https://example.internal/'
    var playerusername = '<ACCOUNT>'
    var usertoken = '<REDACTED>'
    var betrecordurl = 'https://example.internal/'
    var serverurl = 'https://example.internal'
    var betrecordpage = betrecordurl+'?token='+usertoken+'&lang=en&serverurl='+serverurl

    it('environment check', function () {
        cy.visit(homeurl);
    })
    it('1601', function () {
        cy.visit(gameurl+'16slot/?gameid=1601&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個windows的spin按鈕座標，這是舊UI的
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
        //等待account出現
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
        //驗證account名稱是否正確
        cy.get('.table-wrap > #\__BVID__9 > tbody > tr:nth-child(1) > td:nth-child(3)')
          .should('have.value','')
          .should('contain','Garudaman')
        //驗證遊戲名稱
        cy.get('.table-wrap > #\__BVID__9 > tbody > tr:nth-child(1) > td:nth-child(4) > div')
          .should('have.value','')
          .should('contain','1,000')
        //驗證單注遊戲金額，需有千分位號
    })
    it('1602', function () {
        cy.visit(gameurl+'16slot/?gameid=1602&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1603', function () {
        cy.visit(gameurl+'16slot/?gameid=1603&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1604', function () {
        cy.visit(gameurl+'16slot/?gameid=1604&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    // it('1605', function () {
    //     cy.visit(gameurl+'16slot/?gameid=1605&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
    //     cy.wait(30000)
    //     //cy.get('canvas').click(575,525,{ force: true });
    //     cy.get('canvas').click(575,525);
    //     // 第一個視窗
    //     // cy.get('canvas').click(1065,945,{ force: true });
    //     // 第二個視窗
    //     // cy.get('canvas').click(1195,945,{ force: true });
    //     cy.visit(betrecordpage);
    //     cy.get('#app > .home > .record-wrap > .account-wrap > p')
    //       .should('have.value','') 
    //       .should(($p) => {
    //           expect($p).to.contain(playerusername)
    //       })
    // })
    it('1606', function () {
        cy.visit(gameurl+'16slot/?gameid=1606&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1700', function () {
        cy.visit(gameurl+'17scratch/?gameid=1700&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1701', function () {
        cy.visit(gameurl+'17scratch/?gameid=1701&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1811', function () {
        cy.visit(gameurl+'18scratch/?gameid=1811&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(750,570);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1812', function () {
        cy.visit(gameurl+'18scratch/?gameid=1812&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(850,550);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1813', function () {
        cy.visit(gameurl+'18slot/?gameid=1813&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,300);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1815', function () {
        cy.visit(gameurl+'18slot/?gameid=1815&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,300);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1816', function () {
        cy.visit(gameurl+'18slot/?gameid=1816&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,325);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1817', function () {
        cy.visit(gameurl+'18fruit/?gameid=1817&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,350);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1818', function () {
        cy.visit(gameurl+'18slot/?gameid=1818&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(575,525);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1819', function () {
        cy.visit(gameurl+'18slot/?gameid=1819&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,350);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1820', function () {
        cy.visit(gameurl+'18fruit/?gameid=1820&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,350);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1822', function () {
        cy.visit(gameurl+'18slot/?gameid=1822&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(500,575);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1900', function () {
        cy.visit(gameurl+'19slot/?gameid=1900&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1901', function () {
        cy.visit(gameurl+'19slot/?gameid=1901&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1902', function () {
        cy.visit(gameurl+'19slot/?gameid=1902&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1903', function () {
        cy.visit(gameurl+'19slot/?gameid=1903&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1904', function () {
        cy.visit(gameurl+'19slot/?gameid=1904&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1905', function () {
        cy.visit(gameurl+'19slot/?gameid=1905&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('1906', function () {
        cy.visit(gameurl+'19slot/?gameid=1906&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('2000', function () {
        cy.visit(gameurl+'20fruit/?gameid=2000&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('2001', function () {
        cy.visit(gameurl+'20fruit/?gameid=2001&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('2100', function () {
        cy.visit(gameurl+'21fruit/?gameid=2100&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('2101', function () {
        cy.visit(gameurl+'21fruit/?gameid=2101&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('2102', function () {
        cy.visit(gameurl+'21fruit/?gameid=2102&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('2200', function () {
        cy.visit(gameurl+'22slot/?gameid=2200&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
    it('2300', function () {
        cy.visit(gameurl+'23slot/?gameid=2300&token='+usertoken+'&betrecordurl='+betrecordurl+'&lang=en&homeurl=https://localhost&mode=0&serverurl='+serverurl);
        cy.wait(30000)
        //cy.get('canvas').click(575,525,{ force: true });
        cy.get('canvas').click(925,500);
        // 第一個視窗
        // cy.get('canvas').click(1065,945,{ force: true });
        // 第二個視窗
        // cy.get('canvas').click(1195,945,{ force: true });
        cy.visit(betrecordpage);
        cy.get('#app > .home > .record-wrap > .account-wrap > p')
          .should('have.value','') 
          .should(($p) => {
              expect($p).to.contain(playerusername)
          })
    })
})
