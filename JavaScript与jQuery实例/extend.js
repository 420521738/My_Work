(function(){
	jQuery.fn.extend({
		allcheck:function(){
			$(this).find(':checkbox').each(function(){
				this.checked = true;
			})
		},
		
		uncheck:function(){
			$(this).find(':checkbox').each(function(){
				this.checked = false;
			})
		}	

	});
	
	jQuery.extend({
		jallcheck:function(arg){
			$(arg).find(':checkbox').attr('checked','checked')
		},
		
		unjallcheck:function(arg){
			$(arg).find(':checkbox').attr('checked',false)
		}
	})
})()