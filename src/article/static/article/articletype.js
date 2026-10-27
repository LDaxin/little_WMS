// A container and a merge/split article are mutually exclusive (§4d):
// checking one disables the other.
document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("id_article_toggle_space");
    var merge = document.getElementById("id_allow_merge_split");
    if (!toggle || !merge) {
        return;
    }
    function sync() {
        merge.disabled = toggle.checked;
        toggle.disabled = merge.checked;
    }
    toggle.addEventListener("change", sync);
    merge.addEventListener("change", sync);
    sync();
});
