/**
 * 通用选项卡组件（可复用）
 * 使用方式：initTabs('#某个容器选择器')
 * 容器内部结构约定：
 *   .tab-nav li      —— 选项卡导航项
 *   .tab-pane        —— 与导航项一一对应的内容面板
 *   .active          —— 选中状态的类名（可通过第二个参数自定义）
 */

/**
 * 初始化一组选项卡
 * @param {string} boxSelector  选项卡容器选择器，如 '#newsTab'
 * @param {string} activeClass  选中状态类名，默认 'active'
 */
function initTabs(boxSelector, activeClass) {
    activeClass = activeClass || 'active';

    var box = document.querySelector(boxSelector);
    if (!box) return;

    // 获取当前容器内的导航项和内容面板
    var navItems = box.querySelectorAll('.tab-nav li');
    var panes = box.querySelectorAll('.tab-pane');

    // 为每个导航项绑定监听事件
    navItems.forEach(function (item, index) {
        item.addEventListener('click', function () {
            // 第一步：先清除所有选项卡（导航 + 面板）的选中状态
            navItems.forEach(function (nav) {
                nav.classList.remove(activeClass);
            });
            panes.forEach(function (pane) {
                pane.classList.remove(activeClass);
            });

            // 第二步：再设置当前元素的选中状态
            this.classList.add(activeClass);
            panes[index].classList.add(activeClass);
        });
    });
}

// 初始化页面中的新闻选项卡（国内新闻在 HTML 中已设为默认选中）
initTabs('#newsTab');

// 如有其他选项卡，再次调用即可复用，例如：
// initTabs('#videoTab');
// initTabs('#rankTab', 'selected');
