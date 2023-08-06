$("#smartcharthead").on("click",function(){if($("#id_devhead").hasClass('devhead')){$("#id_devhead").removeClass('devhead');}else{$("#id_devhead").addClass('devhead')}});
    $(".devspan span").on("click",function(){let devspana=$(".devspan a");if(devspana.hasClass('show')){devspana.removeClass('show')}else{devspana.addClass('show')}});
    function dev_dassetup(id){
        window.open(`/admin/echart/echartdashboardsetup_v2/${id}/change/?_to_field=id&_popup=1`,`bjsd${id}`,'toolbar=no,scrollbar=no,top=100,left=100,width=900,height=500');
    }
    function dev_dasoption(id){
        window.open(`/echart/option_editor/?dashid=${id}&r=1`,`dsop${id}`,'toolbar=no,scrollbar=no,top=100,left=200,width=500,height=500');
    }
    function dev_dasdivlist(id){
        window.open(`/echart/divlist_editor/?dashid=${id}&r=1`,`dsdiv${id}`,'toolbar=no,scrollbar=no,top=50,left=200,width=800,height=600');
    }
    function dev_daslayout(id){
        window.open(`/echart/template_editor/?dashid=${id}&r=1`,`dsdiv${id}`,'toolbar=no,scrollbar=no,top=50,left=200,width=800,height=600');
    }
    function dev_dasreports(id){
        window.open(`/admin/echart/echartdashboardsetup_v2/${id}/change/?_to_field=id&_popup=1&div=1`,`bjsd${id}`,'toolbar=no,scrollbar=no,top=100,left=100,width=900,height=500');
    }
    function dev_dschartjoin(ec_id,ds_id,chart_type,dsjoin){
        window.open(`/echart/editor_min/?chartid=${ec_id}&dataid=${ds_id}&lc=ec_${chart_type}${dsjoin}&r=1`,`dsj${ec_id}`,'toolbar=no,scrollbar=no,top=100,left=100,width=900,height=500');
    }
    function dev_dschart(ec_id,ds_id,div_id,param_dict,cachestr){
        window.open(`/echart/editor_min/?chartid=${ec_id}&dataid=${ds_id}&divid=${div_id}&param=${param_dict}&cache=${cachestr}&r=1`,`dstx${ds_id}`,'toolbar=no,scrollbar=no,top=100,left=100,width=900,height=500');
    }
    function dev_dseditor(ds_id,div_id,rp_seq,dev_refresh){
        window.open(`/echart/ds_editor/?dsid=${ds_id}&divid=${div_id}&seq=${rp_seq}${dev_refresh}&r=1`,`dskf${ds_id}`,'toolbar=no,scrollbar=no,top=100,left=150,width=800,height=400');
    }
    function dev_dseditord(ds_id,div_id,rp_seq){
        window.open(`/echart/ds_editor/?dsid=${ds_id}&divid=${div_id}&seq=${rp_seq}&on=2`,`dskf${ds_id}`,'toolbar=no,scrollbar=no,top=100,left=150,width=800,height=400');
    }
    function dev_dsdiv(div_id){
        window.open(`/echart/div_editor/?divid=${div_id}&r=1`,`dsdv${div_id}`,'toolbar=no,scrollbar=no,top=100,left=200,width=600,height=400');
    }
