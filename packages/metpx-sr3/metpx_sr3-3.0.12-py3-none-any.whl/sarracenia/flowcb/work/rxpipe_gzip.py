
import gzip
import logging
import os
from sarracenia.flowcb import FlowCB 

logger = logging.getLogger(__name__)


class RxPipe_gzip(FlowCB):

      def __init__(self,options):

          self.o=options
          logger.setLevel(getattr(logging, self.o.logLevel.upper()))
          self.o.add_option( option='rxpipe_name', kind='str' )

      def on_start(self):
          if not hasattr(self.o,'rxpipe_name') and self.o.file_rxpipe_name:
              logger.error("Missing rxpipe_name parameter")
              return
          self.rxpipe = open( self.o.rxpipe_name, "w" )

      def after_work(self, worklist):

          for msg in worklist.ok:
              fname = f'{msg["new_dir"]}/{msg["new_file"]}'
              gzname = f'{fname}.gz'
              if not os.path.exists(gzname) and os.path.exists(fname):
                 # Only try this if the uncompressed file actually exists
                 gzip.open(gzname, 'wb').write(open(fname,'rb').read())
                 os.unlink(fname)
              self.rxpipe.write( msg['new_file'] + '\n' )
          self.rxpipe.flush()
          return None

