/* ============================================================
   文学社社图书模块 —— 选项卡切换逻辑
   作者：张仲涵（zhangzhonghan209）
   说明：所有 JS 变量均以 zzh_ 开头（姓名首字母）
   ============================================================ */

// 页面加载完成后执行初始化（张仲涵）
window.onload = function () {

    // 获取选项卡导航（张仲涵）
    var zzh_tabNav = document.getElementById("zzh_tab_nav");
    // 获取所有选项卡（张仲涵）
    var zzh_tabItems = zzh_tabNav.getElementsByTagName("li");
    // 获取所有图书面板（张仲涵）
    var zzh_panels = document.getElementsByClassName("zzh_panel");
    // 获取所有订阅榜（张仲涵）
    var zzh_ranks = document.getElementsByClassName("zzh_rank");

    // 为每个选项卡绑定点击事件（张仲涵）
    for (var zzh_i = 0; zzh_i < zzh_tabItems.length; zzh_i++) {
        zzh_tabItems[zzh_i].onclick = function () {
            // 通过自定义属性获取当前选项卡的索引（张仲涵）
            var zzh_index = this.getAttribute("data-zzh-index");

            // 第一步：清空所有选项卡的选中状态（张仲涵）
            for (var zzh_j = 0; zzh_j < zzh_tabItems.length; zzh_j++) {
                zzh_tabItems[zzh_j].className = "zzh_tab_item";
            }
            // 第二步：给当前点击的选项卡添加选中状态（张仲涵）
            this.className = "zzh_tab_item zzh_active";

            // 第三步：切换图书面板，只显示对应索引的面板（张仲涵）
            for (var zzh_k = 0; zzh_k < zzh_panels.length; zzh_k++) {
                if (zzh_panels[zzh_k].getAttribute("data-zzh-panel") === zzh_index) {
                    zzh_panels[zzh_k].className = "zzh_panel zzh_show";
                } else {
                    zzh_panels[zzh_k].className = "zzh_panel";
                }
            }

            // 第四步：同步切换右侧订阅榜（张仲涵）
            for (var zzh_m = 0; zzh_m < zzh_ranks.length; zzh_m++) {
                if (zzh_ranks[zzh_m].getAttribute("data-zzh-rank") === zzh_index) {
                    zzh_ranks[zzh_m].className = "zzh_rank zzh_show";
                } else {
                    zzh_ranks[zzh_m].className = "zzh_rank";
                }
            }
        };
    }
};
