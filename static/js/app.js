document.addEventListener('DOMContentLoaded', function(){
  console.log("App JS carregado.");

  // máscara simples para inputs com placeholder (não invasiva)
  document.querySelectorAll('input[name="telefone"]').forEach(function(el){
    el.addEventListener('input', function(e){
      let v = el.value.replace(/\D/g,'');
      if (v.length > 10) v = v.replace(/^(\d{2})(\d{5})(\d{4}).*/,'($1) $2-$3');
      else if (v.length > 5) v = v.replace(/^(\d{2})(\d{4})(\d{0,4}).*/,'($1) $2-$3');
      el.value = v;
    });
  });
});
