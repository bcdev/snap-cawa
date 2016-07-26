package org.esa.snap.dataio.nc4;

import junit.framework.Assert;
import org.esa.snap.core.dataio.ProductIOPlugInManager;
import org.esa.snap.core.dataio.ProductWriterPlugIn;
import org.junit.Test;

import java.util.Iterator;

/**
 * todo: add comment
 * To change this template use File | Settings | File Templates.
 * Date: 11.08.2014
 * Time: 15:04
 *
 * @author olafd
 */
public class SnapCawaNc4WriterLoadedAsServiceTest {
    @Test
    public void testWriterIsLoaded() {
        int writerCount = 0;

        ProductIOPlugInManager plugInManager = ProductIOPlugInManager.getInstance();
        Iterator writerPlugIns = plugInManager.getWriterPlugIns("NetCDF4-CAWA");

        while (writerPlugIns.hasNext()) {
            writerCount++;
            ProductWriterPlugIn plugIn = (ProductWriterPlugIn) writerPlugIns.next();
            System.out.println("writerPlugIn.Class = " + plugIn.getClass());
            System.out.println("writerPlugIn.Descr = " + plugIn.getDescription(null));
        }

        Assert.assertEquals(1, writerCount);

    }

}
