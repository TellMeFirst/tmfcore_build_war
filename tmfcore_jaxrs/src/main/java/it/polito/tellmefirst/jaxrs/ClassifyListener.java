package it.polito.tellmefirst.jaxrs;

import it.polito.tellmefirst.lucene.IndexesUtil;
import static it.polito.tellmefirst.util.TMFUtils.unchecked;
import it.polito.tellmefirst.util.TMFVariables;
import java.io.IOException;
import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;
import javax.servlet.annotation.WebListener;

@WebListener
public class ClassifyListener implements ServletContextListener {

	private TMFVariables variables;

	private void classifyResource() throws IOException {
		variables = new TMFVariables(
			"/var/local/tmfcore/conf/server.properties");
		IndexesUtil.init();
	}
	
	@Override
	public void contextInitialized(ServletContextEvent sce) {
		unchecked( this::classifyResource );
	}

	@Override
	public void contextDestroyed(ServletContextEvent sce) {
	}

}
