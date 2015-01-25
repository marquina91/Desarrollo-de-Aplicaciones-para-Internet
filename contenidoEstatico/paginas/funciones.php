<?php
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////   
/////////////////////////////////////////////barra de LOGIN!1 /////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
function login(){
    
    if(isset($_SESSION['usuario']))
        $_SESSION['usur'] =1;   
        
    else
        $_SESSION['usur'] =0;
        
    if(!$_SESSION['usur'] ){ #---------------------------siNO se esta conectado mostraremos esta barra:
            ?>   
        <section id="barrafija">
                <form action="" method="post"> 
                    <article>
                        <label for="usuario"><p>Nombre:</p></label>
                        <input id="envioD" type="text" name="usuario" id="usuario" required/>
                    </article>

                    <article>
                        <label for="password"><p>Contraseña:</p></label>
                        <input id="envioD" type="text" name="password" id="password" required/>
                    </article>
                        <input id="envio" type="submit" name="enviar" value="Entrar" />
                </form>
                <form action="" method="post"> 
                        <input id="envio" type="submit" name="registro" value="Resgistrarse" />
                </form>
        </section>
<?php
    }  
    else{  #------------------------------------------si esta conectado mostraremos otro tipo de barra:
?>    
        <section id="barrafija">
           <p>Bienvenido, <?php echo $_SESSION['usuario']; ?> </p>                 
                <form action="" method="post"> 
                    <input id="envio"  type="submit" name="out" value="Cerrar Sesi&oacute;n">
                     <?php if($_SESSION['id']==0){ ?> 
                    <input id="envio"  type="submit" name="control" value="Configuraci&oacute;n">                      
                    <?php } ?> 
                </form>
                <?php
                if(isset($_POST['out'])){
                    session_destroy();
                    header("Location: index.php");
                }
                if(isset($_POST['control'])){
                    header("Location: control.php?id=1");
                }
                 ?> 
        </section>
<?php
    }
    
    if(isset($_POST['registro'])){
        header("Location: formulario.php");
    }
    
    if(isset($_POST['enviar'])){
        if($_POST['usuario'] == ' ' || $_POST['password'] == ' '){   //si le da a entrar por error....
            echo'<script>mensaje("Contraseña Incorrecta!")</script>';
        }
            
        else { 
            //$sql = 'SELECT * FROM usuarios'; 
            //$rec = mysql_query($sql); 
            $verificar_usuario = 0; 

           // while($result = mysql_fetch_object($rec)) { /*Devuelve un objeto con propiedades que  corresponden a la tupla recuperada */
            //    if($result->usuario == $_POST['usuario']){ 
                //    $verificar_usuario = 1; 
			if($result->password== $_POST['password']){
                $_SESSION['usur']=1;
                $_SESSION['usuario']=$result->usuario;
                $_SESSION['email']=$result->email;
                $_SESSION['id']=$result->idusuario;
                echo'<script>mensaje("Bienvenido")</script>'; 
                header("Location: index.php");
            }
            else{ 
                echo'<script>mensaje("Contraseña Incorrecta!")</script>'; 
            } 
        } 
    //} 
    if(!$verificar_usuario)
        echo'<script>mensaje("El usuario No existe")</script>';
    }     
}
		s = web.ctx.session
        s.start()
		s.save()
		
		return render.index('Asignatura de DAI','DAI')