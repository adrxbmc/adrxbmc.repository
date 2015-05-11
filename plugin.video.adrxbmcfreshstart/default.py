#------------------------------------------------------------
# Fresh Start # - AdrXbmc - #
#------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# XBMC Add-on for restoring XBMC to its default settings.
# Version 2.0.0
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
AddonID='plugin.video.adrxbmcfreshstart'; AddonTitle="Fresh Start"
import os,sys,plugintools,xbmcaddon
def run(): # Entry point
    plugintools.log("freshstart.run"); params=plugintools.get_params() # Get params
    if params.get("action") is None: main_list(params)
    else: action=params.get("action"); exec action+"(params)"
    plugintools.close_item_list()
def main_list(params): # Main menu
    plugintools.log("freshstart.main_list "+repr(params)); yes_pressed=plugintools.message_yes_no(AddonTitle,"Voce deseja restaurar o seu","Kodi para as configuracoes padrao")
    if yes_pressed:
        addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
        xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("freshstart.main_list xbmcPath="+xbmcPath); failed=False
        try:
            for root, dirs, files in os.walk(xbmcPath,topdown=False):
                for name in files:
                    try: os.remove(os.path.join(root,name))
                    except:
                        if name not in ["Addons15.db","MyVideos75.db","Textures13.db","xbmc.log"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name))
                    except:
                        if name not in ["Database","userdata"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
            if not failed: plugintools.log("freshstart.main_list Todos os arquivos do usuario removido, agora voce tem uma instalacao limpa"); plugintools.message(AddonTitle,"Processo esta concluido, voce esta agora de volta para uma configuracao do Kodi limpa!","Por favor, reinicie o sistema ou reiniciar Kodi para que as alteracoes sejam aplicadas.")
            else: plugintools.log("freshstart.main_list Arquivos do usuario parcialmente removida"); plugintools.message(AddonTitle,"Processo esta concluido, voce esta agora de volta para uma configuracao do Kodi limpa!","Por favor, reinicie o sistema ou reiniciar Kodi para que as alteracoes sejam aplicadas.")
        except: plugintools.message(AddonTitle,"Problema encontrado","As suas definicoes nao foram alteradas"); import traceback; plugintools.log(traceback.format_exc()); plugintools.log("freshstart.main_list NOT removed")
        plugintools.add_item(action="",title="Done",folder=False)
    else: plugintools.message(AddonTitle,"As definicoes","nao foram alteradas"); plugintools.add_item(action="",title="Feito",folder=False)
run()