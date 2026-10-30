/* =========================================================
   main.js  —— 页面交互脚本
   学号：2023xxxxxx   姓名：张仲涵
   功能：下导航页面切换 / 订单页签切换 / 购物车数量增减
   ========================================================= */
(function () {
  'use strict';

  // 学生信息（课程要求：代码中需包含学号或姓名）
  var STUDENT = { id: '2023xxxxxx', name: '张仲涵', cls: '软件工程xx班' };
  console.log('当前项目作者：' + STUDENT.name + '（' + STUDENT.id + '）');

  /* ---------- 1. 下导航切换页面 ---------- */
  var navItems = document.querySelectorAll('#zzhNav .zzh-nav__item');
  var pages = document.querySelectorAll('.zzh-page');

  function activate(name) {
    navItems.forEach(function (n) {
      n.classList.toggle('zzh-nav__item--active', n.getAttribute('data-page') === name);
    });
    pages.forEach(function (p) { p.classList.remove('zzh-page--active'); });
    var page = document.getElementById('page-' + name);
    if (page) { page.classList.add('zzh-page--active'); window.scrollTo(0, 0); }
  }

  navItems.forEach(function (item) {
    item.addEventListener('click', function () {
      var target = item.getAttribute('data-page');
      location.hash = target;   // 支持地址栏直达，如 index.html#cart
      activate(target);
    });
  });

  // 支持 URL hash 直达某个页面，例如 index.html#cart
  var initial = (location.hash || '#home').slice(1);
  if (document.getElementById('page-' + initial)) { activate(initial); }

  /* ---------- 2. 订单页签切换 ---------- */
  document.querySelectorAll('.zzh-orders__tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      document.querySelectorAll('.zzh-orders__tab').forEach(function (t) {
        t.classList.remove('zzh-orders__tab--on');
      });
      tab.classList.add('zzh-orders__tab--on');
    });
  });

  /* ---------- 3. 购物车数量增减 ---------- */
  document.querySelectorAll('.zzh-stepper').forEach(function (step) {
    var num = step.querySelector('span');
    step.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var v = parseInt(num.textContent, 10) || 1;
        num.textContent = btn.textContent === '+' ? v + 1 : Math.max(1, v - 1);
      });
    });
  });

  /* ---------- 4. 购物车选中 ---------- */
  document.querySelectorAll('.zzh-cart-item__check').forEach(function (c) {
    c.addEventListener('click', function () {
      c.classList.toggle('zzh-cart-item__check--on');
    });
  });
})();
